import json
import os
from json import JSONDecodeError

from bottle import route, run, view
from box import Box


# ------- Doomed methods -- to be moved into QUIZ_STORE ----------
def get_quiz_files(directory):
    return [os.path.join(directory, x)
            for x in os.listdir(directory)
            if x.endswith('json')
            ]


def _get_quiz_summaries(quiz_file_paths):
    return [_summary_from_file(filename)
            for filename in quiz_file_paths]


def _summary_from_file(filename):
    with open(filename) as input_file:
        doc = json.load(input_file)
        return ((doc['name']), (doc['title']), filename)

# ------- Doomed methods -- to be moved into QUIZ_STORE ----------

class QuizStore(object):
    def __init__(self):
        self.directories = []
        self.quizzes = []

    def get_quiz_files(self, directory):
        return get_quiz_files(directory)

    def get_quiz_summaries(self, quiz_file_paths):
        return _get_quiz_summaries(quiz_file_paths)



QUIZ_STORE = QuizStore()


@route('/')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology", directory='quizzes'):
    files = QUIZ_STORE.get_quiz_files(directory)
    choices = QUIZ_STORE.get_quiz_summaries(files)
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
    # go get the quiz
    # find the question
    # see if this answer is the right answer
    return True


if __name__ == '__main__':
    run(port=4000, reloader=True, debug=True)
