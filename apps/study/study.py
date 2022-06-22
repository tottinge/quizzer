from typing import Optional

import bottle
from bottle import Bottle, response, view, request

from quizzes.quiz import Quiz
from sessions.session_id import get_client_session_id
from shared.quizzology import Quizzology
from .studycontroller import StudyController

study_controller: Optional[StudyController] = None


def use_this_quizzology(quizzology: Quizzology):
    global study_controller
    study_controller = StudyController(quizzology)


LOOKUP_PATH = ['./apps/study/views', *bottle.TEMPLATE_PATH]

app = Bottle()


@app.route('/')
def menu_of_quizzes(title: str = "Quizzology"):
    """
    Display links to selectable quizzes from quiz store
    """
    summaries = study_controller.get_quiz_summaries()
    return render_menu_of_quizzes(title, summaries)


@view("quiz_selection", template_lookup=LOOKUP_PATH)
def render_menu_of_quizzes(title, choices):
    return dict(title=title, choices=choices)


@app.get('/<quiz_name>')
@view("quiz_question", template_lookup=LOOKUP_PATH)
def get_quiz_first_question(quiz_name: str):
    study_controller.begin_session(response)
    # noinspection PyProtectedMember
    return study_controller.begin_quiz(
        study_controller.get_quiz_by_name(quiz_name)
    )._asdict()


@app.get('/<quiz_name>/<question_number:int>')
@view("quiz_question", template_lookup=LOOKUP_PATH)
def ask_question(quiz_name, question_number) -> dict:
    doc = study_controller.get_quiz_by_name(quiz_name)
    # noinspection PyProtectedMember
    return StudyController.prepare_quiz_question_document(
        doc,
        question_number
    )._asdict()


def url_for(quiz: Quiz, question_number: int):
    return f"/study/{quiz.name}/{question_number}"


@app.post('/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    # pylint disable=no-member
    selection = request.forms.get('answer')
    quiz = study_controller.get_quiz_by_name(quiz_name)
    return render_judgment(quiz, question_number, selection)


@view("quiz_judgment", template_lookup=LOOKUP_PATH)
def render_judgment(quiz: Quiz, question_number: int, selection: str):
    session_id = get_client_session_id(request, response)
    results = study_controller.record_answer_and_get_status(
        question_number, quiz, selection, session_id
    )
    go_next = results.next_question_number
    additions = dict(
        next_url=url_for(quiz, go_next) if go_next else None,
        return_url=url_for(quiz, question_number)
    )
    # noinspection PyProtectedMember
    return {**results._asdict(), **additions}
