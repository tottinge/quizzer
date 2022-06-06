import os
from dataclasses import asdict
from typing import Optional

import pymongo

from quizzes.quiz import Quiz
from quizzes.quiz_store import SaveQuizResult


class QuizStoreMongo:
    def __init__(self, collection_name=None):
        self.collection_name = collection_name if collection_name else 'quizzes'

    def db_connection(self):
        db = pymongo.MongoClient(
            os.environ['QUIZ_MONGO_URL'],
            username=(os.environ['QUIZ_MONGO_USER']),
            password=(os.environ['QUIZ_MONGO_PASSWORD'])
        )
        return db

    def exists(self, quiz_name: str) -> bool:
        with self.db_connection() as db:
            quiz_db = self.collection_name(db)
            result = quiz_db.count_documents({'name': quiz_name})
        return bool(result)

    def collection(self, db):
        return db.quizzology[self.collection_name]

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        with self.db_connection() as db:
            quizzes = self.collection(db)
            try:
                result = quizzes.insert_one(document=asdict(quiz))
                return SaveQuizResult(
                    result.inserted_id,
                    success=True,
                    message=f"quiz [{quiz.name}] saved. Acknowledge: {result.acknowledged}"
                )
            except Exception as err:
                return SaveQuizResult("", False, message=str(err))

    def get_quiz(self, name: str) -> Optional[Quiz]:
        with self.db_connection() as db:
            quizzes = self.collection(db)
            return quizzes.find_one({'name': name})
