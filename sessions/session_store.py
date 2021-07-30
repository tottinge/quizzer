import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Tuple, Set

import tinydb
from tinydb import Query

logger = logging.getLogger(__name__)


@dataclass
class AnswerEntry:
    session_id: str
    quiz_name: str
    question_number: int
    selection: str
    is_correct: bool
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat)

    @classmethod
    def from_dict(cls, dictionary):
        return AnswerEntry(**dictionary)


class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """

    def __init__(self, storage=None):
        self.recorded_answers = []
        self.storage: tinydb.TinyDB = storage

    @staticmethod
    def get_new_session_id():
        import uuid
        return str(uuid.uuid4())

    def record_answer(self, session_id, quiz_name, question_number, selection,
                      is_correct, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().isoformat()
        record = AnswerEntry(session_id, quiz_name, question_number, selection,
                             is_correct, timestamp)
        self.storage.insert(asdict(record))

    def perfect_answers(self, session_id, quiz_name) -> List[AnswerEntry]:
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.quiz_name == quiz_name)
            & (criteria.is_correct == True)
        )
        return [AnswerEntry.from_dict(x) for x in records]

    def incorrect_answers(self, session_id, quiz_name) -> List[AnswerEntry]:
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.quiz_name == quiz_name)
            & (criteria.is_correct == False)
        )
        return [AnswerEntry.from_dict(x) for x in records]

    def number_of_correct_answers(self, session_id, quiz_name) -> int:
        return len(self.perfect_answers(session_id, quiz_name))

    def number_of_incorrect_answers(self, session_id, quiz_name)-> int:
        return len(self.incorrect_answers(session_id, quiz_name))

    def questions_answered_incorrectly(self, session_id) -> Set[Tuple[str, int]]:
        """
        Get a list of questions which were answered incorrectly
        at least once during a session.
        """
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.is_correct == False)
        )
        answers = (AnswerEntry.from_dict(x) for x in records)
        return {(x.quiz_name, x.question_number) for x in answers}

    def questions_answered_correctly(self, target_session):
        """
        Get a list of questions which were never answered incorrectly
        in a given session.
        """
        criteria = Query()
        records = self.storage.search(criteria.session_id == target_session)
        answers = [AnswerEntry.from_dict(x) for x in records]
        total = {(a.quiz_name, a.question_number) for a in answers}
        bad = {(a.quiz_name, a.question_number) for a in answers if
               not a.is_correct}
        return total.difference(bad)

    def get_all(self):
        return self.storage.all()

    def get_log_message(self, session_id, quiz_name,
                        question_number) -> AnswerEntry:
        criteria = Query().fragment({
            'session_id': session_id,
            'quiz_name': quiz_name,
            'question_number': question_number
        })
        records = self.storage.search(criteria)
        return AnswerEntry.from_dict(records[0])

    def shutdown(self):
        logger.critical("Session store: shutting down")
        self.storage.close()
