from json import JSONDecodeError

from bottle import route, run, template, view
from box import Box
import json

@view("main_quiz")
def render_quiz(quiz):
    quiz = Box(quiz)
    return dict(
        title = quiz.title,
        question = quiz.questions[0].question,
        answers = quiz.questions[0].answers
    )


@route('/')
def begin_quiz():
    doc = None
    try:
        with open("quizzes/quiz_doc.json") as quiz:
            doc = json.load(quiz)
    except JSONDecodeError as err:
        print("Quiz file is invalid json")
        raise
    return render_quiz(doc)


if __name__ == '__main__':
    run(reloader=True, debug=True)
