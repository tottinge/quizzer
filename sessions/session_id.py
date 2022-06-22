from uuid import uuid4

SESSION_COOKIE_ID = "qz_current_quiz"


def get_client_session_id(request, response) -> str:
    return request.get_cookie(SESSION_COOKIE_ID) \
           or create_session_id(response)


def create_session_id(response):
    session_id = str(uuid4())
    response.set_cookie(SESSION_COOKIE_ID, session_id, path="/")
    return session_id
