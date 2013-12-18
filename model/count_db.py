import pymongo
from pymongo import MongoClient

### This method prints the number of association rules in for each type (title/body)
def main():
    client = MongoClient()
    db = client.kaggle_facebook
    titles = db.temp1
    body = db.temp2
    print 'titles: '+str(titles.count())+' , body: '+str(body.count())

if __name__ == '__main__':
    main()