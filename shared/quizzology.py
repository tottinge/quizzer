import logging
from os import environ
from typing import Optional

from apps.study.session_store import SessionStore, prepare_session_store
from quizzes.quiz_store_file import QuizStoreFile
from quizzes.quiz_store import QuizStore
from quizzes.quiz_store_mongo import QuizStoreMongo

logger = logging.getLogger(__name__)

class Quizzology:
    """
    Global context object
    All apps that need access to the quizzes and/or session log
    will access them via this "global" instance
    """
    quiz_store: QuizStore
    session_store: SessionStore

    def __init__(self, quiz_store: Optional[QuizStore] = None,
                 session_store: SessionStore = None):
        self.session_store = (session_store
                              if session_store else prepare_session_store())
        if quiz_store:
            selected_store = quiz_store
        elif environ.get('QUIZ_MONGO_URL'):
            selected_store = QuizStoreMongo()
        else:
            selected_store = QuizStoreFile()
        logger.info("Selected quiz store is %s", type(selected_store))
        self.quiz_store: QuizStore = selected_store
