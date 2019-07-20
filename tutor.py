import pymongo
from LessonPlan.parse_syllabus import parse_syllabus
from database.editdb import dbwrite
from Search.searchfor import searchfor
from Search.scrape_smart import open_download
from os import listdir
from os.path import isfile, join
import json
import os
import time
from pprint import pprint
import re

class Tutor():
    def __init__(self):
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=30)
            client.server_info() 
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
            if str(err) == "No servers found yet":
                print('Starting New server on local machine')
        global db
        global subjects
        global topics
        global links_db
        db = client["Tutor"]
        subjects = db["subjects"]
        topics = db["topics"]
        links_db = db["links_db"]
        pass

    def Update_syllabus(self):
        
        syllabus_path = 'Syllabus'
        files = [f for f in listdir(syllabus_path) if isfile(join(syllabus_path, f))]
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.json':
                print("\rSubject is = %s                         " % filename, end='', flush=True)
                with open("{}/{}".format(syllabus_path, file), 'r') as f:
                    subject = json.load(f)
                    subject["Name"] = filename
                    subject["links_synched"] = "false"
                    obj = subjects.find_one_and_update({"Name":filename}, {'$set' : subject}, upsert=True)
        print()
        print("Subjects Synched !")
        print()

    def search_links(self):
        for subject in subjects.find({"links_synched": "false"}):
            print("Subject : {}".format(subject["Name"]))
            for unit in subject["Units"]:
                print("Unit : {}".format(unit))
                for topic in subject["Units"][unit]:
                    trail = " "*(90-len(topic))
                    print("\rTopic is: {}{}".format(topic, trail), end='', flush=True)
                    links = {}
                    i=0
                    time.sleep(2)
                    for link in searchfor(self, subject["Name"], unit, topic):
                        links["{}".format(i)] = link
                        i+=1
                    topics.find_one_and_update({"Name": topic}, {
                                               '$set': {"subject": subject["Name"], "unit": unit, "links": links, "links_synched": "false"}}, upsert=True)
                print()
            print()        
            subjects.find_one_and_update({"Name":subject["Name"]}, {'$set' : {"links_synched" : "true"}})
        print("Links Synched !")
        print()

    def download_links(self):
        link_save_path = "Links"
        for topic in topics.find({"links_synched": "false"}):
            buffer = []
            for link in topic["links"]:
                for dikt in link:
                    pprint(topic["links"][dikt])
                    array = topic["links"][dikt]
                    name = re.sub(r'(?is):.+', '', topic["Name"])                    
                    try:
                        doc, processed_url, found = open_download(
                            self, topic=name, buffer=buffer, filedir=dikt, link=array[-1])
                        if not processed_url in buffer:
                            buffer.append(processed_url)
                    except IndexError:
                        continue
                    time.sleep(5)
                    if found:
                        print("found")
                        links_db.find_one_and_update({"Name": "{} {}".format(topic["Name"], array[-1])},{
                            '$set': {"path": "{}/{}/{}/{}".format(link_save_path, name, dikt, doc), "Name": doc, "synched": "false"}}, upsert=True)
                    else:
                        print("could not process")
                        topic["links"][dikt] = ""
                        topics.find_one_and_update({"Name": topic["Name"]}, {'$set': topic})
            topics.find_one_and_update({"Name": topic["Name"]}, {'$set': {"links_synched" : "true"}})        

    
    def links2notes(self):
        for subject, unit, topic in parse_syllabus(self, path=syllabus_path):
            print("reading syllabus")
            raw_notes = []
            for link in dbread(self, subject, unit, topic):
                raw_notes.append(parse_link(link))
            notes_write(self, subject, unit, topic, notes=raw_notes)

    def book2notes(self):
        for subject_lib in syllabus(self, path=syllabus_path):
            print("reading syllabus")
            for book in subject_lib:
                textbook = readbook(self, book, subject_lib)
                for unit in readunit(self, textbook):
                    topics = unit_topic(self, unit, textbook)
                    for topic in topics:
                        sum1 = summarizer1(topic, unit ,textbook)
                        sum2 = summarizer2(topic, unit ,textbook)
                        sum3 = summarizer3(topic, unit ,textbook)
                        sum_books(self, sum1, sum2,sum3, unit, textbook, subject_lib)

    def merge_notes():
        for subject, unit, topic in parse_syllabus(self, path=syllabus_path):
            print("reading syllabus")
            mix_notes(self, subject, unit, topic)

    def beautify_notes():
        for notes, save_name in readmxnotes:
            if notes.tobeautify:
                outfile = beautify(notes)
                with open ("Out/{}".format(save_name), 'w') as o:
                    o.write(outfile)

    def test2notes(self):
        for subject, unit in unit_syllabus(self, path=syllabus_path):
            print("reading syllabus")
            for Q, A in parse_tests(self, subject, unit):
                problemwrite(self, Q, A, subject, unit)

    def gen_test(self):
        problems, soln, hint, test_number = get_test(self, numberofQ, subject, unit, topic="All")
        print("Find your Questions in folder %s " % test_number)

    def eval_test(self):
        test_number = input("Enter test_number")
        print("Make sure that your answer is in the folder ProblemSets/{}/Answers".format(test_number))
        time.sleep(15)
        print("Reading answer", end="")
        while(i<20):
            print(".", end="")
            time.sleep(0.125)
        print('')
        score, comment = process_answers(test_number)
        print("Your Score is : {} , {}".format(score, comment))

    def gen_ques(self):
        for subject, unit in unit_syllabus(self, path=syllabus_path):
            print("reading notes")
            notes = read_mix_notes(self, subject, unit, topic="All")
            for Q, A in frame_questions(notes):
                problemwrite(self, Q, A, subject, unit)

    def video2notes(self):
        for subject, unit, topic in parse_syllabus(self, path=syllabus_path):
            print("searching for {}: {}".format(unit, topic))
            links = []
            for link in video_search(self, subject, unit, topic):
                links.append(link)
            viddbwrite(self, subject, unit, topic, links=links)

    def scheduler(self):
        schedule = g_getschedule(self, date)
        try:
            tasks = g_missed_tasks(self, date, schedule)
            print("Found {} incomplete tasks".format(tasks.length))
            print("Pushing to Schedule Queue............")
            schedule_queue.push(tasks)
        except IndexError as error:
            print("No Missed Tasks")
        
        try:
            if schedule_queue:
                date, time = find_DT(schedule_queue, schedule)
                assign(self, date, time)
                print("Assigning {} tasks to schedule".format(schedule_queue.length))           
        except IndexError as error:
            print("Schedule Queue Empty !")


    def taskmaster(self):
        try:
            for chunk in load_chunk_queue():
                tasks = process_chunks(chunk)
                schedule_queue.push(tasks)
                self.scheduler()
        except IndexError as error:
            print("No Chunks left to Assing !")

    def make_chunks(self):
        schedule = g_getschedule(self, date)
        for subject in syllabus:
            for division in subject_division(subject, divDBpath):
                for unit, topic in division:
                    chunks = rapp(self, topic, unit, division, subject, schedule)
                    push2chunkQ(chunk)

   


if __name__ == "__main__":
    tut = Tutor()
    #tut.Update_syllabus()
    #tut.search_links()
    #tut.download_links()
