import os
from typing import Dict
from urllib.parse import urlencode

import jwt
from bottle import redirect, request
from jwt import ExpiredSignatureError, DecodeError, InvalidSignatureError


def login(flash="", destination="/study"):
    url = build_login_url(
        destination=destination,
        flash=flash
    )
    redirect(url)


def build_login_url(**vargs):
    parts = ['/login']
    if vargs:
        parts.append(urlencode(vargs))
    return "?".join(parts)


def require_roles(*required_roles):
    """Decorator function factory, captures roles"""
    required_roles = required_roles or ['guest']

    def inner_wrapper(wrapped_function):
        """Wrapper generator for route or  function that will be restricted"""

        def decorator(*args, **kwargs):
            """check authorization before actually calling route function"""
            try:
                user_data = get_current_user()
                role = user_data.get('role', 'guest')
                if role not in required_roles:
                    name = user_data.get('user_name')
                    login(
                        f'Sorry, {name}, you are just a {role}',
                        destination=get_request_path()
                    )
                return wrapped_function(*args, **kwargs)
            except AttributeError:
                login('You must be logged in to access this page')
            except ExpiredSignatureError:
                login(flash='Your session has expired',
                      destination=get_request_path())
            except InvalidSignatureError:
                login(flash='Your session was created on a different server',
                      destination=get_request_path())
            except DecodeError:
                redirect('/login')

        return decorator
    return inner_wrapper


def get_current_user() -> Dict:
    token = get_authorization_token()
    user_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return user_data


def get_request_path():
    return request.path


def get_authorization_token():
    _, token = request.get_cookie('Authorization').split()
    return token


SECRET_KEY = os.environ.get('QUIZZOLOGY_KEY', 'hardcoded_nonsense')
