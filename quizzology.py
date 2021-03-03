from quiz import Quiz

# Future home of the Quizzology object
from quiz_store import QuizStore
from session_store import SessionStore


class Quizzology:
    quiz_store = None
    session_store = None

    def set_quiz_store(self, new_store: QuizStore):
        self.quiz_store = new_store

    def get_quiz_store(self) -> QuizStore:
        return self.quiz_store

    def set_session_store(self, session_store: SessionStore):
        self.session_store = session_store

    def get_session_store(self) -> SessionStore:
        return self.session_store

    def get_quiz_summaries(self) -> list:
        return self.quiz_store.get_quiz_summaries()

    def get_quiz_by_name(self, quiz_name: str) -> Quiz:
        return self.get_quiz_store().get_quiz(quiz_name)