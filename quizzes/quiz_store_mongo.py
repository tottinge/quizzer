import os
from dataclasses import asdict
from typing import Optional, Iterable

import pymongo

from quizzes.quiz import Quiz
from quizzes.quiz_store import SaveQuizResult, QuizSummary


def db_connection():
    db = pymongo.MongoClient(
        os.environ['QUIZ_MONGO_URL'],
        username=os.environ.get('QUIZ_MONGO_USER', ''),
        password=os.environ.get('QUIZ_MONGO_PASSWORD', '')
    )
    return db


class QuizStoreMongo:
    def __init__(self, collection_name=None):
        self.collection_name = collection_name if collection_name else 'quizzes'

    def exists(self, quiz_name: str) -> bool:
        with db_connection() as db:
            quiz_db = self.collection_name(db)
            result = quiz_db.count_documents({'name': quiz_name})
        return bool(result)

    def collection(self, db: pymongo.MongoClient) -> pymongo.collection:
        return db.quizzology[self.collection_name]

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        with db_connection() as db:
            quizzes = self.collection(db)
            try:
                result = quizzes.find_one_and_update(
                    {"name": quiz.name},
                    {'$set': asdict(quiz)},
                    upsert=True
                )
                return SaveQuizResult(
                    result.inserted_id,
                    success=True,
                    message=(f"quiz [{quiz.name}] saved. "
                             f"Acknowledge: {result.acknowledged}")
                )
            except Exception as err:
                return SaveQuizResult("", False, message=str(err))

    def get_quiz(self, name: str) -> Optional[Quiz]:
        with db_connection() as db:
            quizzes = self.collection(db)
            found = quizzes.find_one({'name': name})
            if found:
                return Quiz.from_json(found)

    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        with db_connection() as db:
            quizzes: pymongo.collection = self.collection(db)
            result = []
            for item in quizzes.find({}, {'name': 1, 'title': 1, '_id': 1}):
                result.append(QuizSummary(
                    name=item['name'],
                    title=item['title'],
                    id=item["_id"]
                ))
            return result
