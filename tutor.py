from LessonPlan.parse_syllabus import parse_syllabus
from database.editdb import dbwrite
from Search.searchfor import searchfor
import json
import os
import time

class Tutor():
    def __init__(self):
        pass

    def syllabus(self):
        syllabus_path = 'Syllabus'
        for subject, unit, topic in parse_syllabus(self, path=syllabus_path):
            print("searching for {}: {}".format(unit, topic))
            links = []
            for link in searchfor(self, subject, unit, topic):
                links.append(link)
            dbwrite(self, subject, unit, topic, links=links)

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
    tut.links2notes()