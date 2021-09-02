from quizzes.quiz_store import QuizStore
from sessions.session_store import SessionStore


class Quizzology:
    """
    Global context object
    All apps that need access to the quizzes and/or session log
    will access them via this "global" instance
    """
    def __init__(self, quiz_store: QuizStore, session_store: SessionStore):
        self.session_store = session_store
        self.quiz_store = quiz_store