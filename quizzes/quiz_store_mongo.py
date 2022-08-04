import os
from dataclasses import asdict
from typing import Optional, Iterable

import pymongo

from quizzes.quiz import Quiz
from quizzes.quiz_store import SaveQuizResult, QuizSummary
from quizzes.quiz_store_file import QuizStoreFile
from shared.mongo_connection import db_connection


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
            desired_fields = {
                'name': 1,
                'title': 1,
                '_id': 1,
                'image_url': 1
            }
            for item in quizzes.find({}, desired_fields):
                summary = QuizSummary(
                    name=item['name'],
                    title=item['title'],
                    id=item["_id"],
                    image_url=item.get('image_url', './favicon.ico'))
                result.append(summary)
            return result


def import_from_files():
    file_store: QuizStoreFile = QuizStoreFile()
    mongo_store: QuizStoreMongo = QuizStoreMongo()
    for summary in file_store.get_quiz_summaries():
        quiz = file_store.get_quiz(summary.name)
        mongo_store.save_quiz(quiz)

