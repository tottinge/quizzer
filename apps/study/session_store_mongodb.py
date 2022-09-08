from dataclasses import asdict
from typing import List, Iterable

from apps.study.session_store import SessionStore, AnswerEntry
from shared.mongo_connection import db_connection


class SessionStoreMongoDB(SessionStore):
    def record_answer(self, session_id, quiz_name, question_number, selection,
                      is_correct, question_id, timestamp=None):
        entry = AnswerEntry(
            session_id, 
            quiz_name, 
            question_number, 
            selection,
            is_correct, 
            question_id, 
            timestamp)
        with db_connection() as db:
            collection = db['quizzology']['log']
            collection.add(asdict(entry))

    def perfect_answers(self, session_id, quiz_name) -> List[AnswerEntry]:
        pass

    def number_of_incorrect_answers(self, session_id, quiz_name) -> int:
        pass

    def get_all(self) -> Iterable[AnswerEntry]:
        pass

    def get_log_message(self, session_id, quiz_name,
                        question_number) -> AnswerEntry:
        pass