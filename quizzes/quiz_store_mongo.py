import os

import pymongo


class MongoFileStore:

    def __init__(self):
        self.url = os.environ['QUIZ_MONGO_URL']
        self.username = os.environ['QUIZ_MONGO_USER']
        self.password = os.environ['QUIZ_MONGO_PASSWORD']

    def exists(self, quiz_name: str) -> bool:
        db_connection = pymongo.MongoClient(self.url,
                                            username=self.username,
                                            password=self.password)

        quiz_db = db_connection['quizzology']['quizzes']
        result = quiz_db.count_documents({'name': quiz_name})
        db_connection.close()
        return bool(result)
