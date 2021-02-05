""" Whee. This is the main routine!"""
import os
from logging import getLogger

from bottle import (
    route, run, view, request, post, get, response, static_file
)
from tinydb import TinyDB

from quiz_store import QuizStore
from session_store import SessionStore

QUIZ_STORE = QuizStore()
SESSION_STORE = None

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
        choices=QUIZ_STORE.get_quiz_summaries()
    )

@route('/favicon.ico')
def get_favicon():
    return static_file("favicon.ico", root="./static")

@route('/static/<filename>')
def get_static_file(filename):
    rootpath = os.environ.get('STATIC_PATH', './static/')
    return static_file(filename, root=rootpath)


@get('/quizzes/<quiz_name>/<question_number:int>')
def ask_question(quiz_name, question_number):
    doc = QUIZ_STORE.get_quiz(quiz_name)
    return render_question(doc, question_number)


@view("quiz_question")
def render_question(quiz, question_number=0):
    selected_question = quiz.questions[question_number] \
        if quiz.questions \
        else {}
    total_questions = len(quiz.questions)
    return dict(
        title=quiz.title,
        progress=int(((question_number + 1) / total_questions) * 100),
        total_questions=total_questions,
        question_number=question_number,
        quiz_name=quiz.name,
        question=selected_question.question,
        decoys=selected_question.get("decoys", None),
        answer=selected_question.get("answer", None),
        resources=(selected_question.get("resources"))
    )


@post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = QUIZ_STORE.get_quiz(quiz_name)
    return render_judgment(quiz, question_number, selection)


@view("quiz_judgment")
def render_judgment(quiz, question_number, selection):
    question = quiz.questions[question_number]
    correct = is_answer_correct(question, selection)
    quiz_name = quiz.name
    total_questions = len(quiz.questions)
    progress = int(((question_number + 1) / total_questions) * 100)
    return_url = f"/quizzes/{quiz_name}/{question_number}"
    next_number = quiz.next_question_number(question_number)
    next_url = f"/quizzes/{quiz_name}/{next_number}" if next_number else None

    logger.info("getting id")
    id = get_client_session_id(request, response)
    logger.info("Recording answer")
    SESSION_STORE.record_answer(id, quiz_name, question_number, selection,
                                correct)
    logger.info("On like usual...")
    return dict(
        title=quiz.title,
        total_questions=total_questions,
        question_number=question_number,
        correct=correct,
        selection=selection,
        incorrect_answers=SESSION_STORE.number_of_incorrect_answers("DOOMED",
                                                                    quiz_name),
        progress=progress,
        next_url=next_url,
        return_url=return_url
    )


def is_answer_correct(question: object, chosen: object) -> object:
    return chosen == question.answer


@get("/me")
def show_me():
    "Junk method for exploring the session environment variables. Delete at will."
    # Display information about the session environment
    # return request.environ.get('REMOTE_ADDR')
    fwd_for = request.environ.get("HTTP_X_FORWARDED_FOR","not listed in HTTP_X-forwarded")
    remote = request.environ.get('REMOTE_ADDR', "not listed in remote addr") 
    whoareyou = request.environ.get("HTTP_X_FORWARDED_FOR","").split(" ")[-1] \
                or request.environ.get('REMOTE_ADDR') \
                or "a ninja"
    print("Remote route", request.remote_route)
    vars = (f"<span>{key}: {value}</span><br>"
            for (key, value) in
            sorted(list(request.environ.items()))
            )
    return (
        f"<p>Maybe you're {fwd_for}, and maybe you're {remote}.</p>"
        + f"<p>I'm guessing you are {whoareyou}.</p>" 
        + "".join(vars)
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
        for answer in SESSION_STORE.storage.all()
    ]
    return "<br>".join(text_answers)


def get_client_session_id(request, response):
    id = request.get_cookie(SESSION_COOKIE_ID)
    if not id:
        id = SESSION_STORE.get_new_session_id()
        response.set_cookie(SESSION_COOKIE_ID, id, path="/")
    return id


def drop_client_session_id(response):
    response.delete_cookie(SESSION_COOKIE_ID, path="/")


def main():
    global SESSION_STORE
    SESSION_STORE = prepare_session_store()
    host_name, port_number = get_endpoint_address()
    run(host=host_name, port=port_number, reloader=True, debug=True)


def get_endpoint_address():
    host_name = os.environ.get('QUIZ_HOST', '0.0.0.0')
    heroku_port = os.environ.get('PORT', '4000')
    port_number = int(os.environ.get('QUIZ_PORT', heroku_port))
    return host_name, port_number


def prepare_session_store():
    path, filename = os.path.split(PATH_TO_LOG_DB)
    if not os.path.exists(path):
        os.makedirs(path)
    return SessionStore(TinyDB(PATH_TO_LOG_DB))


if __name__ == '__main__':
    main()
