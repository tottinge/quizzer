from uuid import uuid4

SESSION_COOKIE_ID = "qz_current_quiz"


def drop_client_session_id(response):
    response.delete_cookie(SESSION_COOKIE_ID, path="/")


def get_client_session_id(request, response) -> str:
    session_id = request.get_cookie(SESSION_COOKIE_ID)
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(SESSION_COOKIE_ID, session_id, path="/")
    return session_id
