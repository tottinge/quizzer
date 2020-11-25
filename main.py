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
def render_question(quiz):
    quiz = Box(quiz)
    q = quiz.questions and quiz.questions[0] or {}
    resources = q.get("resources")
    return dict(
        title=quiz.title,
        question=q.question,
        decoys=q.decoys,
        answer=q.answer,
        resources=resources
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


def answer_question(quiz, question, choice):
    # go get the quiz
    # find the question
    # see if this answer is the right answer
    return True


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
