import os
from logging import getLogger
import json
from json import JSONDecodeError

from bottle import route, run, view
from box import Box

logger = getLogger(__name__)

class QuizStore(object):
    """ For consideration
    * why keep passing directories around?
    * why not do a dirwalk?
    * instead of filename, an ID in summaries?
    """

    def __init__(self):
        self.quiz_dir = 'quizzes'

    def get_quiz_summaries(self):
        return self._get_quiz_summaries_from_file_list(
            self._get_quiz_files_from_directory(self.quiz_dir)
        )

    def get_quiz(self, quiz_name):
        filename = self._find_file_for_named_quiz(quiz_name)
        return self._read_quiz_document(filename)

    def _get_quiz_files_from_directory(self, directory):
        try:
            return [os.path.join(directory, x)
                    for x in os.listdir(directory)
                    if x.endswith('json')
                    ]
        except FileNotFoundError as error:
            logger.error(f"reading quiz directory: {error}")
            return []


    def _get_quiz_summaries_from_file_list(self, quiz_file_paths):
        def get_name_title_filename_from(quiz_filename):
            document = self._read_quiz_doc_from_file(quiz_filename)
            return document['name'], document['title'], quiz_filename

        return [get_name_title_filename_from(filename)
                for filename in quiz_file_paths]

    def _quiz_summaries_for(self, directory):
        return self._get_quiz_summaries_from_file_list(self._get_quiz_files_from_directory(directory))

    def _read_quiz_doc_from_file(self, filename):
        with open(filename) as input_file:
            return json.load(input_file)

    def _find_file_for_named_quiz(self, quiz_name):
        lookup = {
            name: filename
                  for (name, _, filename)
                  in self.get_quiz_summaries()
        }
        filename = lookup.get(quiz_name)
        return filename

    def _read_quiz_document(self, filename):
        return self._read_quiz_doc_from_file(filename)


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
