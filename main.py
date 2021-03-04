""" Whee. This is the main routine!"""
import os
from logging import getLogger

from bottle import (
    route, run, view, request, post, get, response, static_file, redirect
)
from tinydb import TinyDB

from quiz import Question
from quiz_store import QuizStore
from quizzology import Quizzology
from session_store import SessionStore

quizzology = Quizzology()

SESSION_COOKIE_ID = "qz_current_quiz"
logger = getLogger(__name__)
PATH_TO_LOG_DB = "logs/session_log.json"


@route('/')
@route('/quizzes')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology"):
    response.delete_cookie(SESSION_COOKIE_ID)
    return dict(
        title=title,
        choices=quizzology.get_quiz_summaries()
    )


@route('/favicon.ico')
def get_favicon():
    return redirect("/static/favicon.ico")


@route('/static/<filename>')
def get_static_file(filename):
    rootpath = os.environ.get('STATIC_PATH', './static/')
    return static_file(filename, root=rootpath)


@get('/quizzes/<quiz_name>/<question_number:int>')
def ask_question(quiz_name, question_number):
    doc = quizzology.get_quiz_by_name(quiz_name)
    return render_question(doc, question_number)


@view("quiz_question")
def render_question(quiz, question_number=0):
    selected_question = quiz.question_by_number(question_number) \
        if quiz.has_questions() \
        else Question({})
    total_questions = quiz.number_of_questions()
    return dict(
        title=quiz.title,
        progress=int(((question_number + 1) / total_questions) * 100),
        total_questions=total_questions,
        question_number=question_number,
        quiz_name=quiz.name,
        question=selected_question.question,
        decoys=selected_question.decoys,
        answer=selected_question.answer,
        resources=selected_question.resources
    )


@post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = quizzology.get_quiz_by_name(quiz_name)
    return render_judgment(quiz, question_number, selection)


@view("quiz_judgment")
def render_judgment(quiz, question_number, selection):
    question = quiz.question_by_number(question_number)
    correct = is_answer_correct(question, selection)
    quiz_name = quiz.name
    total_questions = len(quiz.questions)
    progress = int(((question_number + 1) / total_questions) * 100)
    return_url = f"/quizzes/{quiz_name}/{question_number}"
    next_number = quiz.next_question_number(question_number)
    next_url = f"/quizzes/{quiz_name}/{next_number}" if next_number else None

    logger.info("getting id")
    session_id = get_client_session_id(request, response)
    logger.info("Recording answer")
    quizzology.get_session_store().record_answer(session_id, quiz_name, question_number,
                                selection,
                                correct)
    logger.info("On like usual...")
    incorrect_answers = quizzology.get_session_store().number_of_incorrect_answers(session_id,
                                                                  quiz_name)
    return dict(
        title=quiz.title,
        total_questions=total_questions,
        question_number=question_number,
        correct=correct,
        selection=selection,
        incorrect_answers=incorrect_answers,
        progress=progress,
        next_url=next_url,
        return_url=return_url
    )


def is_answer_correct(question: Question, chosen: str) -> bool:
    return question.is_correct_answer(chosen)


@get("/me")
def show_me():
    "Junk method for exploring the session environment variables. Delete at will."
    # Display information about the session environment
    # return request.environ.get('REMOTE_ADDR')
    fwd_for = request.environ.get("HTTP_X_FORWARDED_FOR",
                                  "not listed in HTTP_X-forwarded")
    remote = request.environ.get('REMOTE_ADDR', "not listed in remote addr")
    whoareyou = request.environ.get("HTTP_X_FORWARDED_FOR", "").split(" ")[-1] \
                or request.environ.get('REMOTE_ADDR') \
                or "a ninja"
    print("Remote route", request.remote_route)
    env_vars = (f"<span>{key}: {value}</span><br>"
                for (key, value) in
                sorted(list(request.environ.items()))
                )
    return (
            f"<p>Maybe you're {fwd_for}, and maybe you're {remote}.</p>"
            + f"<p>I'm guessing you are {whoareyou}.</p>"
            + "".join(env_vars)
    )


@get("/cookies")
def cookie_explorer():
    "Junk method for exploring cookies. Delete at will."
    result = "".join(
        f"<p>{key}: {value}</p>" for (key, value) in request.cookies.items())
    return result


@get("/session")
def show_session():
    from string import Template
    template = Template(
        "$timestamp $session_id\t"
        "$quiz_name:$question_number\t"
        "$is_correct\t"
        "'$selection'"
    )
    text_answers = [
        template.substitute(answer)
        for answer in quizzology.get_session_store().storage.all()
    ]
    return "<br>".join(text_answers)


def get_client_session_id(request, response):
    session_id = request.get_cookie(SESSION_COOKIE_ID)
    if not session_id:
        session_id = quizzology.get_session_store().get_new_session_id()
        response.set_cookie(SESSION_COOKIE_ID, session_id, path="/")
    return session_id


def drop_client_session_id(response):
    response.delete_cookie(SESSION_COOKIE_ID, path="/")


def main():
    store = QuizStore()
    quizzology.set_quiz_store(store)
    quizzology.set_session_store(prepare_session_store())
    host_name, port_number = get_endpoint_address()
    run(host=host_name, port=port_number, reloader=True, debug=True)


def get_endpoint_address():
    host_name = os.environ.get('QUIZ_HOST', '0.0.0.0')
    heroku_port = os.environ.get('PORT', '4000')
    port_number = int(os.environ.get('QUIZ_PORT', heroku_port))
    return host_name, port_number


def prepare_session_store():
    path = os.path.dirname(PATH_TO_LOG_DB)
    if not os.path.exists(path):
        os.makedirs(path)
    return SessionStore(TinyDB(PATH_TO_LOG_DB))


if __name__ == '__main__':
    main()
