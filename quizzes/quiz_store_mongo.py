import os
from dataclasses import asdict

import pymongo

from quizzes.quiz import Quiz
from quizzes.quiz_store import SaveQuizResult


class QuizStoreMongo:
    def __init__(self, db_name=None):
        self.collection = db_name if db_name else 'Quizzology'
        self.url = os.environ['QUIZ_MONGO_URL']
        self.username = os.environ['QUIZ_MONGO_USER']
        self.password = os.environ['QUIZ_MONGO_PASSWORD']

    def db_connection(self):
        return pymongo.MongoClient(
            self.url,
            username=self.username,
            password=self.password
        )

    def exists(self, quiz_name: str) -> bool:
        with self.db_connection() as db:
            quiz_db = db[self.collection]['quizzes']
            result = quiz_db.count_documents({'name': quiz_name})
        return bool(result)

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        with self.db_connection() as db:
            quizzes = db[self.collection]['quizzes']
            try:
                result = quizzes.insert_one(document=asdict(quiz))
                return SaveQuizResult(
                    result.inserted_id,
                    success=True,
                    message=f"quiz [{quiz.name}] saved. Acknowledge: {result.acknowledged}"
                )
            except Exception as err:
                return SaveQuizResult("", False, message=str(err))
