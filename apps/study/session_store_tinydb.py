from dataclasses import asdict
from datetime import datetime
from typing import List, Set, Tuple

import tinydb
from tinydb import Query

from apps.study.session_store import SessionStore, AnswerEntry


class SessionStoreTinyDB(SessionStore):
    """
    Store user sessions for later analysis and reporting
    """

    def __init__(self, storage=None):
        self.storage: tinydb.TinyDB = storage

    def record_answer(self, session_id, quiz_name, question_number, selection,
                      is_correct, question_id, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().isoformat()
        record = AnswerEntry(session_id, quiz_name, question_number, selection,
                             is_correct, question_id, timestamp)
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

    def number_of_incorrect_answers(self, session_id, quiz_name) -> int:
        return len(self.incorrect_answers(session_id, quiz_name))

    def questions_answered_incorrectly(self, session_id) -> Set[
        Tuple[str, int]]:
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
