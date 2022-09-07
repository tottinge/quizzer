from pymongo import MongoClient
from os import environ

def db_connection() -> MongoClient:
    return MongoClient(
        host=environ['QUIZ_MONGO_URL'],
        username=environ.get('QUIZ_MONGO_USER', ''),
        password=environ.get('QUIZ_MONGO_PASSWORD', '')
    )