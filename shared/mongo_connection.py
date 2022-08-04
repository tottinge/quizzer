import pymongo
from os import environ

def db_connection():
    db = pymongo.MongoClient(
        environ['QUIZ_MONGO_URL'],
        username=environ.get('QUIZ_MONGO_USER', ''),
        password=environ.get('QUIZ_MONGO_PASSWORD', '')
    )
    return db