import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

import click
import pymongo

@click.command()
@click.option("--mongo", default="mongodb://hotp:hotp7890@220.100.163.134/hotp?authSource=hotp")
@click.option("--db_name", default="hotp")
@click.option("--collection", default="hotp_geoposts")
def run(mongo, db_name, collection):
    conn = pymongo.MongoClient(mongo)
    db   = conn[db_name]

    docs = db[collection].find({"PostCaptionText.text":{"$exists":True}})
    print("We have %s in total" % docs.count())
    for index, doc in enumerate(docs):
        print("Processing: {}".format((index+1)))
        db[collection].update({"_id": doc["_id"]}, {"$set":{"PostCaptionText": doc["PostCaptionText"]["text"]}})
    after_count = db[collection].count({"PostCaptionText.text": {"$exists": True}})
    print("After: %s" % after_count)
    conn.close()

if __name__ == "__main__":
    run()