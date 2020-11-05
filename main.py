import os
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

@view("quiz_selection")
def render_menu_of_quizzes(title):
    return dict(title=title)

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

def get_test_files(directory):
    return [ os.path.join(directory,x)
             for x in os.listdir(directory)
             if x.endswith('json')
             ]

def get_test_summary(quiz_file_paths):
    return [('pass', 'a tests that passes', 'd/pass.json')
            for q in quiz_file_paths]


if __name__ == '__main__':
    run(reloader=True, debug=True)
