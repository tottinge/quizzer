class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """
    def __init__(self):
        self.recorded_answers = []
        
    def record_answer(self, session_id, quiz_name, question_number, selection, is_correct):
        self.recorded_answers.append( (session_id, quiz_name, question_number, selection, is_correct))

    def perfect_answers(self, session_id, quiz_name):
        return [ item for item in self.recorded_answers
                 if item[-1] == True and item[1] == quiz_name and item[0] == session_id]

    def incorrect_answers(self, session_id, quiz_name):
        return [ item for item in self.recorded_answers
                 if item[-1] == False and item[1] == quiz_name and item[0] == session_id]

    def number_of_correct_answers(self, session_id, quiz_name):
        return len(self.perfect_answers(session_id, quiz_name))

    def number_of_incorrect_answers(self, session_id, quiz_name):
        return len(self.incorrect_answers(session_id, quiz_name))

    def get_new_session_id(self):
        import uuid
        return str(uuid.uuid4())
    