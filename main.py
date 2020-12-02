import os
from logging import getLogger
import json
from json import JSONDecodeError

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
        choices=(QUIZ_STORE._quiz_summaries_for(directory))
    )


@view("quiz_question")
def render_question(quiz, question_number=0):
    quiz = Box(quiz)
    selected_question = quiz.questions \
                        and quiz.questions[question_number] \
                        or {}
    return dict(
        title=quiz.title,
        question=selected_question.question,
        decoys=selected_question.decoys,
        answer=selected_question.answer,
        resources=(selected_question.get("resources"))
    )


@route('/<dirname>/<filename>')
def begin_quiz(dirname, filename):
    """
    * Shouldn't read files; use QuizStore
    * Shouldn't receive file path, name, but just an ID for QuizStore
    """
    doc = None
    try:
        filename = os.path.join(dirname, filename)
        with open(filename) as quiz:
            doc = json.load(quiz)
    except JSONDecodeError as err:
        print("Quiz file is invalid json")
        raise
    return render_question(doc)

@route('/quizzes/<quiz_name>/<question_number:int>')
def replacement_for_begin_quiz_above(quiz_name, question_number):
    print(f"Getting q:{question_number} of {quiz_name}")
    doc = QUIZ_STORE.get_quiz(quiz_name)
    print(doc['title'], doc['name'], doc['questions'][question_number])
    return render_question(doc, int(question_number))

def answer_question(quiz, question, choice):
    # go get the quiz
    # find the question
    # see if this answer is the right answer
    return True


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
