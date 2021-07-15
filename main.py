""" 
main.py - start and run the Bottle-based quizzology application.py

Uses environment variables:
* STATIC_PATH: location of static resources (default './static/')
* 'QUIZ_HOST' IP address the Bottle server will bind to (default '0.0.0.0')
* 'PORT' port set by HEROKU server (default '4000')
* 'QUIZ_PORT', port used by quizzology (default: see 'PORT')

Main doesn't take any command line parameters, and launches a web server
that serves up quizzes and tracks answers.

"""
import os
import signal
from logging import getLogger

import bottle
from bottle import (
    run, view, request, response, static_file, redirect
)
from tinydb import TinyDB

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology, SESSION_COOKIE_ID
from sessions.session_store import SessionStore

quizzology = Quizzology()

logger = getLogger(__name__)
PATH_TO_LOG_DB = "logs/session_log.json"  # Misplaced?

from beaker import middleware

app = middleware.SessionMiddleware(bottle.app(), {})


@bottle.route('/')
@bottle.route('/quizzes')
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


@bottle.route('/favicon.ico')
def get_favicon():
    return redirect("/static/favicon.ico")


@bottle.route('/static/<filename>')
def get_static_file(filename):
    root_path = os.environ.get('STATIC_PATH', './static/')
    return static_file(filename, root=root_path)


@bottle.get('/quizzes/<quiz_name>')
@view("quiz_question")
def start_quizzing(quiz_name):
    return quizzology.begin_quiz(
        quizzology.get_quiz_by_name(quiz_name))._asdict()


@bottle.get('/quizzes/<quiz_name>/<question_number:int>')
@view("quiz_question")
def ask_question(quiz_name, question_number) -> dict:
    doc = quizzology.get_quiz_by_name(quiz_name)
    return Quizzology.prepare_quiz_question_document(doc,
                                                     question_number)._asdict()


@bottle.route('/edit')
@view('quiz_authoring_form')
def do_nothing_interesting():
    return {
        'quiz': Quiz('name', 'title'),
        'title': "ignore me i'm new"
    }


@bottle.post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = quizzology.get_quiz_by_name(quiz_name)
    return render_judgment(quiz, question_number, selection)


def url_for(quiz: Quiz, question_number: int):
    return f"/quizzes/{quiz.name}/{question_number}"


@view("quiz_judgment")
def render_judgment(quiz: Quiz, question_number: int, selection: str):
    session_id = get_client_session_id(request, response)
    results = quizzology.record_answer_and_get_status(
        question_number, quiz, selection, session_id
    )

    # Todo: Figure out how to use the session middleware
    # app.session['answer'] = results.selection, results.correct

    go_next = results.next_question_number
    additions = dict(
        next_url=url_for(quiz, go_next) if go_next else None,
        return_url=url_for(quiz, question_number)
    )
    return {**results._asdict(), **additions}


@bottle.get("/me")
def show_me():
    """ 
    Test endpoint: this routine will display information about the 
    session environment. It's probably not recommended for production
    use - it's hard to say what opportunities it leaves hackers.
    """
    REMOTE_ADDR = 'REMOTE_ADDR'
    FORWARDED_FOR = "HTTP_X_FORWARDED_FOR"

    fwd_for = request.environ.get(FORWARDED_FOR,
                                  "not listed in HTTP_X-forwarded")
    remote = request.environ.get(REMOTE_ADDR, "not listed in remote addr")
    last_fwd_addr = request.environ.get(FORWARDED_FOR, "").split(" ")[-1]
    who_are_you = last_fwd_addr \
                  or request.environ.get(REMOTE_ADDR) \
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


@bottle.get("/cookies")
def cookie_explorer():
    """
    Junk method for exploring cookies; not part of quizzology proper, 
    only used by authors for peeking into the world of the server and
    understanding how cookies work.
    """
    result = "".join(
        f"<p>{key}: {value}</p>" for (key, value) in request.cookies.items())
    return result


@bottle.get("/session")
def show_session():
    """
    Show session logs: for troubleshooting.
    """
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
    beaker_session = [
        f"<p>{key}, {value}</p>\n"
        for (key, value) in app.session
    ] if app.session else 'none'
    beaker_section = '<div>Beaker: ' + "".join(beaker_session) + "</div>"

    return "<br>".join(text_answers) + beaker_section


def get_client_session_id(request, response) -> str:
    session_id = request.get_cookie(SESSION_COOKIE_ID)
    if not session_id:
        session_id = quizzology.new_session_id()
        response.set_cookie(SESSION_COOKIE_ID, session_id, path="/")
    return session_id


def drop_client_session_id(response):
    response.delete_cookie(SESSION_COOKIE_ID, path="/")


def main():
    quizzology.set_quiz_store(QuizStore())
    quizzology.set_session_store(prepare_session_store())
    host_name, port_number = get_endpoint_address()
    run(app, host=host_name, port=port_number, reloader=True, debug=True)


def get_endpoint_address() -> tuple[str, int]:
    host_name = os.environ.get('QUIZ_HOST', '0.0.0.0')
    heroku_port = os.environ.get('PORT', '4000')
    port_number = int(os.environ.get('QUIZ_PORT', heroku_port))
    return host_name, port_number


def prepare_session_store() -> SessionStore:
    path = os.path.dirname(PATH_TO_LOG_DB)
    if not os.path.exists(path):
        os.makedirs(path)
    return SessionStore(TinyDB(PATH_TO_LOG_DB))


def shutdown(signum, frame):
    logger.critical(f'Received shutdown signal {signum}')
    quizzology.shutdown()
    exit(0)


signal.signal(signal.SIGTERM, shutdown)

if __name__ == '__main__':
    main()
