from typing import Optional

from apps.study.session_store import SessionStore, prepare_session_store
from quizzes.quiz_store_file import QuizStoreFile
from quizzes.quiz_store import StoresQuizzes


class Quizzology:
    """
    Global context object
    All apps that need access to the quizzes and/or session log
    will access them via this "global" instance
    """
    quiz_store: StoresQuizzes
    session_store: SessionStore

    def __init__(self, quiz_store: Optional[StoresQuizzes] = None,
                 session_store: SessionStore = None):
        self.session_store = (session_store
                              if session_store else prepare_session_store())
        self.quiz_store: StoresQuizzes = quiz_store \
            if quiz_store else QuizStoreFile()
