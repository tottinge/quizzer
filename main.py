""" Whee. This is the main routine!"""
import os
from logging import getLogger

from bottle import (
    route, run, view, request, post, get, response, static_file, redirect
)
from tinydb import TinyDB

from quiz_store import QuizStore
from quizzology import Quizzology, SESSION_COOKIE_ID
from sessions.session_store import SessionStore

quizzology = Quizzology()

logger = getLogger(__name__)
PATH_TO_LOG_DB = "logs/session_log.json"  # Misplaced?


@route('/')
@route('/quizzes')
def menu_of_quizzes(title="Quizzology"):
    quizzology.begin_session(response)
    summaries = quizzology.get_quiz_summaries()
    return render_menu_of_quizzes(title, summaries)

@view("quiz_selection")
def render_menu_of_quizzes(title, choices):
    return dict(title=title, choices=choices)

@route('/favicon.ico')
def get_favicon():
    return redirect("/static/favicon.ico")


@route('/static/<filename>')
def get_static_file(filename):
    root_path = os.environ.get('STATIC_PATH', './static/')
    return static_file(filename, root=root_path)


@get('/quizzes/<quiz_name>/<question_number:int>')
@view("quiz_question")
def ask_question(quiz_name, question_number):
    doc = quizzology.get_quiz_by_name(quiz_name)
    return Quizzology.prepare_quiz_question_document(doc, question_number)


@post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = quizzology.get_quiz_by_name(quiz_name)
    return render_judgment(quiz, question_number, selection)

def url_for(quiz, question_number):
    return f"/quizzes/{quiz.name}/{question_number}"

@view("quiz_judgment")
def render_judgment(quiz, question_number, selection):
    return get_answer_results(question_number, quiz, selection)

#TODO -- Continue looking at moving this and that dependant methods to Quizzology
def get_answer_results(question_number, quiz, selection):
    question = quiz.question_by_number(question_number)
    correct = question.is_correct_answer(selection)
    next_number = quiz.next_question_number(question_number)
    session_id = get_client_session_id(request, response)
    quizzology.record_answer(session_id, quiz.name, question_number, selection,
                             correct, None)
    incorrect_answers = quizzology.number_of_incorrect_answers(quiz.name,
                                                               session_id)
    return dict(
        quiz=quiz,
        title=quiz.title,
        question_number=question_number,
        correct=correct,
        selection=selection,
        incorrect_answers=incorrect_answers,
        next_url=(url_for(quiz, next_number) if next_number else None),
        return_url=(url_for(quiz, question_number))
    )


@get("/me")
def show_me():
    # Display information about the session environment
    # return request.environ.get('REMOTE_ADDR')
    fwd_for = request.environ.get("HTTP_X_FORWARDED_FOR",
                                  "not listed in HTTP_X-forwarded")
    remote = request.environ.get('REMOTE_ADDR', "not listed in remote addr")
    who_are_you = request.environ.get("HTTP_X_FORWARDED_FOR", "").split(" ")[-1] \
        or request.environ.get('REMOTE_ADDR') \
        or "a ninja"
    print("Remote route", request.remote_route)
    env_vars = (f"<span>{key}: {value}</span><br>"
                for (key, value) in
                sorted(list(request.environ.items()))
                )
    return (
            f"<p>Maybe you're {fwd_for}, and maybe you're {remote}.</p>"
            + f"<p>I'm guessing you are {who_are_you}.</p>"
            + "".join(env_vars)
    )


@get("/cookies")
def cookie_explorer():
    """Junk method for exploring cookies. Delete at will."""
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
        for answer in quizzology.get_log_messages()
    ]
    return "<br>".join(text_answers)


def get_client_session_id(request, response):
    session_id = request.get_cookie(SESSION_COOKIE_ID)
    if not session_id:
        session_id = quizzology.new_session_id()
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
