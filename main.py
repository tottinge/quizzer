from logging import getLogger

from bottle import route, run, view, request, post, get

from quiz_store import QuizStore

logger = getLogger(__name__)

QUIZ_STORE = QuizStore()


@route('/')
@route('/quizzes')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology"):
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
    selected_question = quiz.questions \
                        and quiz.questions[question_number] \
                        or {}
    return dict(
        title=quiz.title,
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
    return_url = f"/quizzes/{quiz_name}/{question_number}"
    next_url = None
    next_number = quiz.next_question_number(question_number)
    if next_number is not None:
        next_url = f"/quizzes/{quiz_name}/{next_number}"
    return dict(
        title=quiz.title,
        correct=correct,
        selection=selection,
        next_url=next_url,
        return_url=return_url
    )


def is_answer_correct(question: object, chosen: object) -> object:
    return chosen == question.answer


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
