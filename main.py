import json
import os
from json import JSONDecodeError

from bottle import route, run, view
from box import Box

@route('/')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology", directory='quizzes'):
    files = get_quiz_files(directory)
    choices = get_quiz_summary(files)
    return dict(
        title=title,
        choices=choices
    )


@view("quiz_question")
def render_question(quiz):
    quiz = Box(quiz)
    q = quiz.questions and quiz.questions[0] or {}
    r = q.get("resources")
    return dict(
        title=quiz.title,
        question=q.question,
        answers=q.answers,
        resources=r
    )


@route('/<dirname>/<filename>')
def begin_quiz(dirname, filename):
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
    return None



def get_quiz_files(directory):
    """
    Find the files in a given directory (not doing dirwalk)
    which end in '.json'
    """
    return [os.path.join(directory, x)
            for x in os.listdir(directory)
            if x.endswith('json')
            ]


def get_quiz_summary(quiz_file_paths):
    """
    Collect a list containing test name, title (description), and filename
    from a given directory of json files
    For use in selecting a quiz.txt
    """
    return [_summary_from_file(filename)
            for filename in quiz_file_paths]

def _summary_from_file(filename):
    with open(filename) as input_file:
        doc = json.load(input_file)
        return ((doc['name']), (doc['title']), filename)


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
