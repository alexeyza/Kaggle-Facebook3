import pymongo
from pymongo import MongoClient

def main():
    client = MongoClient()
    db = client.kaggle_facebook
    collection = db.temp1
    print collection.count()
#    res = collection.find({'score':{'$gte':0.6}})
#    for r in res:
#        print r['tag']

if __name__ == '__main__':
    main()