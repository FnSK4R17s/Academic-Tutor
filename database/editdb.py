from os import listdir
from os.path import isfile, join
import json
import os

def dbwrite(self, subject, unit, topic, links=['no links yet'], dbpath='database', dbfile='db.json'):
    
    unt = {
        topic: links
    }
    sub = {
        unit: unt
    }
    
    app = {
        subject: sub
    }

    try:
        with open ("{}/{}".format(dbpath, dbfile), 'r') as db:
            data = json.load(db)
    except json.decoder.JSONDecodeError as error:
        print(error)
        data = app

    
    
    #print(data[subject][unit][topic])

    try:
        if data[subject]:
            try:
                if data[subject][unit]:
                    try:
                        if data[subject][unit][topic]:
                            print("Adding Links to Database")
                            data[subject][unit].update({
                                topic: links
                            })
                    except KeyError as error:
                        print("New Topic")
                        data[subject][unit].update(unt)
            except KeyError as error:
                print("New Unit")
                data[subject].update(sub)
    except KeyError as error:
        print("New Subject")
        data.update(app)
    with open ("{}/{}".format(dbpath, dbfile), 'w') as db:
        json.dump(data, db)