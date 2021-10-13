from quizzes.quiz_store import QuizStore
from apps.study.session_store import SessionStore, prepare_session_store


class Quizzology:
    """
    Global context object
    All apps that need access to the quizzes and/or session log
    will access them via this "global" instance
    """
    def __init__(self, quiz_store: QuizStore = None,
                 session_store: SessionStore = None):
        self.session_store = (session_store
                              if session_store else prepare_session_store())
        self.quiz_store = quiz_store if quiz_store else QuizStore()

