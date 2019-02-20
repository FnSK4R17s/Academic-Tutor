from os import listdir
from os.path import isfile, join
import json
import os

#returns each topic from the given syllabus path
def parse_syllabus(self, path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.json':
                print("Subject is = %s" % filename)
                with open("{}/{}".format(path, file), 'r') as f:
                    data = json.load(f)
                    for unit in data:
                        for _ in data[unit]:
                            print(unit)
                            for j in data[unit][_]:
                                print(j)
                                yield filename, unit, j