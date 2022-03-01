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
from logging import getLogger, Logger

import bottle
from bottle import (
    run, request, static_file, redirect
)

from apps.author.author import app as authoring_app
from apps.study.study import app as quizzing_app
from apps.study.study import use_this_quizzology as study_use
from security.authn import make_bearer_token, authenticate
from security.authz import require_roles
from shared.quizzology import Quizzology

HOME_PAGE = '/study'

logger: Logger = getLogger(__name__)
app = bottle.app()

quizzology = Quizzology()
study_use(quizzology)


app.mount('/author', authoring_app)
app.mount('/study', quizzing_app)


@app.route('/login')
@bottle.view("login")
def login():
    return {
        "title": "Who are you?",
        "flash": request.query.get("flash", ""),
        "destination": request.query.get("destination", "")
    }


@app.post('/auth')
def authentication_endpoint():
    data: bottle.FormsDict = request.forms
    user_name = data.get('user_name')
    password = data.get('password')
    user = authenticate(user_name, password)
    if not user:
        return login("Your credentials did not match any on file.")
    bottle.response.set_cookie('Authorization',
                               f"Bearer {make_bearer_token(user)}",
                               httponly=True)
    bottle.response.set_cookie('qz-user-name', user.user_name)
    bottle.response.set_cookie('qz-user-role', user.role)
    destination = request.forms.get('destination')
    redirect(destination or HOME_PAGE)


@app.route('/')
def menu_of_quizzes():
    redirect('/login')


@app.route('/favicon.ico')
def get_favicon():
    return get_static_file('favicon.ico')


@app.route('/static/<filename>')
def retrieve_file(filename):
    return get_static_file(filename)


def get_static_file(filename):
    root_path = os.environ.get('STATIC_PATH', './static/')
    return static_file(filename, root=root_path)


@app.get("/me")
def show_me():
    """
    Test endpoint: this routine will display information about the
    session environment. It's probably not recommended for production
    use - it's hard to say what opportunities it leaves hackers.
    """
    remote_addr_header = 'REMOTE_ADDR'
    x_forward_header = "HTTP_X_FORWARDED_FOR"

    fwd_for = request.environ.get(x_forward_header,
                                  "not listed in HTTP_X-forwarded")
    remote = request.environ.get(remote_addr_header,
                                 "not listed in remote addr")
    last_fwd_addr = request.environ.get(x_forward_header, "").split(" ")[-1]
    who_are_you = (
            last_fwd_addr
            or request.environ.get(remote_addr_header)
            or "a ninja"
    )
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


@app.get("/cookies")
def cookie_explorer():
    """
    Junk method for exploring cookies; not part of quizzology proper,
    only used by authors for peeking into the world of the server and
    understanding how cookies work.
    """
    cookies: bottle.FormsDict = request.cookies
    result = "".join(
        f"<p>{key}: {value}</p>" for (key, value) in cookies.items())
    return result


@app.get("/session")
@require_roles('student', 'author')
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
    from apps.study.study import study_controller
    text_answers = [
        template.substitute(answer)
        for answer in study_controller.get_log_messages()
    ]
    return "<br>".join(text_answers)


def main():
    host_name, port_number = get_endpoint_address()
    run(
        app,
        host=host_name,
        port=port_number,
        server='auto',
        reloader=True,
        debug=True
    )


def get_endpoint_address() -> tuple[str, int]:
    host_name = os.environ.get('QUIZ_HOST', '0.0.0.0')
    heroku_port = os.environ.get('PORT', '4000')
    port_number = int(os.environ.get('QUIZ_PORT', heroku_port))
    return host_name, port_number


if __name__ == '__main__':
    main()

# Require user to authenticate (a form with a POST w/username & pw) ✓
# When they authenticate, we create and store a JWT ✓
# We decorate the routes that need authentication
# Magic happens ...
# If authenticated (where is tht stored?) it enters the route ✓
# if not authenticated, it redirects to the login screen? ✓
# We need to know user/password/role, etc. ✓
# { userid, password, [author|student|?] role, friendly name?, ? }
