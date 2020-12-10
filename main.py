from logging import getLogger

from bottle import route, run, view, request, post, get
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


@get('/quizzes/<quiz_name>/<question_number:int>')
def ask_question(quiz_name, question_number):
    doc = QUIZ_STORE.get_quiz(quiz_name)
    return render_question(doc, question_number)

@post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = QUIZ_STORE(quiz_name)
    question = quiz['questions'][question_number]
    render_judgment(question, selection)

def render_judgment(question, selection):
    correct = is_answer_correct(question, selection)
    judgment = correct and "correct" or "not what we're looking for"
    return f"Answer is [{selection}], which is {judgment}."


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


def is_answer_correct(question, chosen):
    return chosen == question['answer']


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
