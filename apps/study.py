import os

from bottle import Bottle, response, view
from tinydb import TinyDB

from quizzes.quiz_store import QuizStore
from quizzology import Quizzology
from sessions.session_store import SessionStore

quizzology = Quizzology()


def setup_quizzology():
    quizzology.set_quiz_store(QuizStore())
    quizzology.set_session_store(prepare_session_store())


PATH_TO_LOG_DB = "logs/session_log.json"  # Misplaced?


def prepare_session_store() -> SessionStore:
    path = os.path.dirname(PATH_TO_LOG_DB)
    if not os.path.exists(path):
        os.makedirs(path)
    return SessionStore(TinyDB(PATH_TO_LOG_DB))


setup_quizzology()
app = Bottle()


@app.route('/')
def menu_of_quizzes(title: str = "Quizzology"):
    """
    Display links to selectable quizzes from quiz store
    """
    quizzology.begin_session(response)
    summaries = quizzology.get_quiz_summaries()
    return render_menu_of_quizzes(title, summaries)


@view("quiz_selection")
def render_menu_of_quizzes(title, choices):
    return dict(title=title, choices=choices)
