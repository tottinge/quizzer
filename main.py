""" Whee. This is the main routine!"""
from logging import getLogger, DEBUG

from bottle import route, run, view, request, post, get, response
from tinydb import TinyDB

from quiz_store import QuizStore
from session_store import SessionStore, AnswerEntry

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


@get('/quizzes/<quiz_name>/<question_number:int>')
def ask_question(quiz_name, question_number):
    doc = QUIZ_STORE.get_quiz(quiz_name)
    return render_question(doc, question_number)


@view("quiz_question")
def render_question(quiz, question_number=0):
    selected_question = quiz.questions[question_number] if quiz.questions else {}
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
    SESSION_STORE.record_answer(id, quiz_name, question_number, selection, correct)
    logger.info("On like usual...")
    return dict(
        title=quiz.title,
        total_questions=total_questions,
        question_number=question_number,
        correct=correct,
        selection=selection,
        incorrect_answers=SESSION_STORE.number_of_incorrect_answers("DOOMED", quiz_name),
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
    print("Remote route", request.remote_route)
    return "".join(f"<p>{key}: {value}</p>" for (key, value) in list(request.environ.items()))


@get("/cookies")
def cookie_explorer():
    "Junk method for exploring cookies. Delete at will."
    result = "".join(f"<p>{key}: {value}</p>" for (key, value) in request.cookies.items())
    return result


@get("/session")
def show_session():
    text_answers = [
        "{} {} {} {} {} '{}'".format(
            a.timestamp,
            a.session_id,
            a.quiz_name,
            a.question_number,
            a.is_correct,
            a.selection
        )
        for a in (
            AnswerEntry.from_dict(x)
            for x in SESSION_STORE.storage.all()
        )
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
    global QUIZ_STORE, SESSION_STORE
    SESSION_STORE = SessionStore(TinyDB(PATH_TO_LOG_DB))
    logger.setLevel(DEBUG)
    run(port=4000, reloader=True, debug=True)


if __name__ == '__main__':
    main()
