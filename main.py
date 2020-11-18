import json
import os
from json import JSONDecodeError

from bottle import route, run, view
from box import Box

class QuizStore(object):

    def get_quiz_files(self, directory):
        return [os.path.join(directory, x)
                    for x in os.listdir(directory)
                    if x.endswith('json')
                    ]

    def get_quiz_summaries(self, quiz_file_paths):
        return [self._summary_from_file(filename)
                for filename in quiz_file_paths]

    def _summary_from_file(self, filename):
        with open(filename) as input_file:
            doc = json.load(input_file)
            return ((doc['name']), (doc['title']), filename)

    def quiz_summaries_for(self, directory):
        return self.get_quiz_summaries(self.get_quiz_files(directory))



QUIZ_STORE = QuizStore()


@route('/')
@view("quiz_selection")
def render_menu_of_quizzes(title="Quizzology", directory='quizzes'):
    return dict(
        title=title,
        choices=(QUIZ_STORE.quiz_summaries_for(directory))
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
