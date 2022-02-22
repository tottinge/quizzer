import jwt
from bottle import redirect, request
from jwt import ExpiredSignatureError, DecodeError


def login(flash="", destination="/study"):
    url = "/login"
    redirect(url)


def require_roles(*required_roles):
    """Decorator function factory, captures roles"""
    required_roles = required_roles or ['guest']

    def inner_wrapper(wrapped_function):
        """Wrapper generator for route or  function that will be restricted"""

        def decorator(*args, **kwargs):
            """check authorization before actually calling route function"""
            try:
                token = get_authorization_token()
                user_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                role = user_data.get('role', 'guest')
                if role not in required_roles:
                    name = user_data.get('user_name')
                    return login(
                        f'Sorry, {name}, you are just a {role}',
                        destination=get_request_path()
                    )
                return wrapped_function(*args, **kwargs)
            except AttributeError:
                return login('You must be logged in to access this page')
            except ExpiredSignatureError:
                return login(flash='Your session has expired',
                             destination=get_request_path())
            except DecodeError:
                redirect('/login')

        return decorator

    return inner_wrapper


def get_request_path():
    return request.path


def get_authorization_token():
    _, token = request.get_cookie('Authorization').split()
    return token


SECRET_KEY = 'hardcoded_nonsense'
