from typing import List

from apps.study.session_store import SessionStore, AnswerEntry


class SessionStoreMongoDB(SessionStore):
    def perfect_answers(self, session_id, quiz_name) -> List[AnswerEntry]:
        pass

    def number_of_incorrect_answers(self, session_id, quiz_name):
        pass

    def get_all(self):
        pass

    def get_log_message(self, session_id, quiz_name, question_number):
        pass

    def record_answer(self, session_id, quiz_name, question_number, selection,
                      is_correct, question_id, timestamp=None):
        pass


