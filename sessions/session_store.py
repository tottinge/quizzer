import logging
from datetime import datetime

import tinydb
from tinydb import Query

logger = logging.getLogger(__name__)

class AnswerEntry:
    """
    Record an answer given to a question in a test session.
    Whole-value class allows for evolution of records without breaking existing code.
    """

    def __init__(self, session_id, quiz_name, question_number, selection, is_correct, timestamp=None):
        self.session_id = session_id
        self.quiz_name = quiz_name
        self.question_number = question_number
        self.selection = selection
        self.is_correct = is_correct
        self.timestamp = timestamp or datetime.now().isoformat()

    def __eq__(self, other):
        return (
                self.timestamp == other.timestamp
                and self.session_id == other.session_id
                and self.quiz_name == other.quiz_name
                and self.question_number == other.question_number
                and self.selection == other.selection
                and self.is_correct == other.is_correct
        )

    def as_dict(self):
        return dict(
            timestamp=self.timestamp,
            session_id=self.session_id,
            quiz_name=self.quiz_name,
            question_number=self.question_number,
            selection=self.selection,
            is_correct=self.is_correct
        )

    @classmethod
    def from_dict(cls, record):
        return AnswerEntry(session_id=record["session_id"],
                           quiz_name=record["quiz_name"],
                           question_number=record["question_number"],
                           selection=record["selection"],
                           is_correct=record["is_correct"],
                           timestamp=record.get("timestamp", None))


class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """

    def __init__(self, storage=None):
        self.recorded_answers = []
        self.storage : tinydb.TinyDB = storage

    @staticmethod
    def get_new_session_id():
        import uuid
        return str(uuid.uuid4())

    def record_answer(self, session_id, quiz_name, question_number, selection, is_correct, timestamp=None):
        record = AnswerEntry(session_id, quiz_name, question_number, selection, is_correct, timestamp)
        self.storage.insert(record.as_dict())

    def perfect_answers(self, session_id, quiz_name):
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.quiz_name == quiz_name)
            & (criteria.is_correct == True)
        )
        return [AnswerEntry.from_dict(x) for x in records]

    def incorrect_answers(self, session_id, quiz_name):
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.quiz_name == quiz_name)
            & (criteria.is_correct == False)
        )
        return [AnswerEntry.from_dict(x) for x in records]

    def number_of_correct_answers(self, session_id, quiz_name):
        return len(self.perfect_answers(session_id, quiz_name))

    def number_of_incorrect_answers(self, session_id, quiz_name):
        return len(self.incorrect_answers(session_id, quiz_name))

    def questions_answered_incorrectly(self, target_session):
        """
        Get a list of questions which were answered incorrectly
        at least once during a session.
        """
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == target_session)
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
        bad = {(a.quiz_name, a.question_number) for a in answers if not a.is_correct}
        return total.difference(bad)

    def get_all(self):
        return self.storage.all()

    def get_log_message(self, session_id, quiz_name, question_number)->AnswerEntry:
        criteria = Query()
        records = self.storage.search(
            (criteria.session_id == session_id)
            & (criteria.quiz_name == quiz_name)
            & (criteria.question_number == question_number)
        )
        return AnswerEntry.from_dict(records[0])

    def shutdown(self):
        logger.critical("Session store: shutting down")
        self.storage.close()

