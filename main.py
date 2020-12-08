from logging import getLogger

from bottle import route, run, view
from box import Box

from quiz_store import QuizStore

logger = getLogger(__name__)

QUIZ_STORE = QuizStore()


@route('/')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology", directory='quizzes'):
    return dict(
        title=title,
        # Todo : This is the wrong function -- it's private and knows directories.
        choices=(QUIZ_STORE._quiz_summaries_for(directory))
    )


@route('/quizzes/<quiz_name>/<question_number:int>')
def quiz_question(quiz_name, question_number):
    doc = QUIZ_STORE.get_quiz(quiz_name)
    return render_question(doc, question_number)


@view("quiz_question")
def render_question(quiz, question_number=0):
    quiz = Box(quiz)
    selected_question = quiz.questions \
                        and quiz.questions[question_number] \
                        or {}
    return dict(
        title=quiz.title,
        question=selected_question.question,
        decoys=selected_question.get("decoys", None),
        answer=selected_question.get("answer", None),
        resources=(selected_question.get("resources"))
    )


def answer_question(quiz_name, question_number, chosen):
    quiz = QUIZ_STORE.get_quiz(quiz_name)
    question = quiz.get('questions')[question_number]
    return chosen == question['answer']


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
