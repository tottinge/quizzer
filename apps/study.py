import os

from bottle import Bottle, response, view, request
from tinydb import TinyDB

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology
from sessions.session_id import get_client_session_id
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


@app.get('/<quiz_name>')
@view("quiz_question")
def get_quiz_first_question(quiz_name: str):
    return quizzology.begin_quiz(
        quizzology.get_quiz_by_name(quiz_name)
    )._asdict()


@app.get('/<quiz_name>/<question_number:int>')
@view("quiz_question")
def ask_question(quiz_name, question_number) -> dict:
    doc = quizzology.get_quiz_by_name(quiz_name)
    # noinspection PyProtectedMember
    return Quizzology.prepare_quiz_question_document(
        doc,
        question_number
    )._asdict()


def url_for(quiz: Quiz, question_number: int):
    return f"/study/{quiz.name}/{question_number}"


@app.post('/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = quizzology.get_quiz_by_name(quiz_name)
    return render_judgment(quiz, question_number, selection)


@view("quiz_judgment")
def render_judgment(quiz: Quiz, question_number: int, selection: str):
    session_id = get_client_session_id(request, response)
    results = quizzology.record_answer_and_get_status(
        question_number, quiz, selection, session_id
    )
    go_next = results.next_question_number
    additions = dict(
        next_url=url_for(quiz, go_next) if go_next else None,
        return_url=url_for(quiz, question_number)
    )
    return {**results._asdict(), **additions}
