class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """

    def __init__(self):
        self.recorded_answers = []

    def record_answer(self, session_id, quiz_name, question_number, selection, is_correct):
        record = (session_id, quiz_name, question_number, selection, is_correct)
        self.recorded_answers.append(record)

    def perfect_answers(self, session_id, quiz_name):
        return [item for item in self.recorded_answers
                if item[0] == session_id and item[-1] is True]

    def incorrect_answers(self, session_id, quiz_name):
        return [item for item in self.recorded_answers
                if item[0] == session_id and item[-1] is False]

    def number_of_correct_answers(self, session_id, quiz_name):
        return len(self.perfect_answers(session_id, quiz_name))

    def number_of_incorrect_answers(self, session_id, quiz_name):
        return len(self.incorrect_answers(session_id, quiz_name))

    @staticmethod
    def get_new_session_id():
        import uuid
        return str(uuid.uuid4())
