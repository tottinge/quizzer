from dataclasses import asdict
from datetime import datetime
from typing import List, Iterable

from apps.study.session_store import SessionStore, AnswerEntry
from shared.mongo_connection import db_connection


class Session:
    session_id: str
    quiz_id: str
    user_id: str
    created_time: datetime  # updated at begin_session
    completed_time: datetime  # updated at render_judgement if no next url
    events: List[AnswerEntry]

# Todo: move from TinyDB to MongoDB
# implement the mongo db store
# excise tinyDB completely
# expand session store to store actual sessions, not just activities
# all in preparation for the coming session review and resume work
# and eventually the cohort conglomeration of sessions

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
