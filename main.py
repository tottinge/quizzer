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


@post('/quizzes/<quiz_name>/<question_number:int>')
def check_answer(quiz_name, question_number):
    selection = request.forms.get('answer')
    quiz = QUIZ_STORE.get_quiz(quiz_name)
    title = quiz['title']
    question = quiz['questions'][question_number]
    return render_judgment(quiz, 0, selection)


@view("quiz_judgment")
def render_judgment(quiz, question_number, selection):
    question = quiz['questions'][question_number]
    judgment = is_answer_correct(question, selection) \
               and "correct" \
               or "not what we're looking for"
    quiz_name = quiz['name']
    url = f"/quizzes/{quiz_name}/{question_number}"
    # Did you pass
    # if you fail - can you retry
    # if there's another question - advance
    # else display end of quiz page
    return dict(
        title=quiz['title'],
        text=f"Answer is [{selection}], which is {judgment}.",
        url=url
    )




def is_answer_correct(question: object, chosen: object) -> object:
    return chosen == question['answer']


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
