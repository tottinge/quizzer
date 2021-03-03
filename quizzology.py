# Future home of the Quizzology object
class Quizzology:
    quiz_store = None
    session_store = None

    def set_quiz_store(self, new_store):
        self.quiz_store = new_store

    def get_quiz_store(self):
        return self.quiz_store

    def set_session_store(self, session_store):
        self.session_store = session_store

    def get_session_store(self):
        return self.session_store

    def get_quiz_summaries(self):
        return self.quiz_store.get_quiz_summaries()

    def get_quiz_by_name(self, quiz_name):
        doc = self.get_quiz_store().get_quiz(quiz_name)