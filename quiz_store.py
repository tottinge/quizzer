import json
import os
from json import JSONDecodeError
from logging import getLogger

from quiz import Quiz

logger = getLogger(__name__)


class QuizStore:
    """ For consideration
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
        document = self._read_quiz_document(filename)
        return Quiz(document) if document else None

    def _get_quiz_files_from_directory(self, directory):
        try:
            return [os.path.join(directory, x)
                    for x in os.listdir(directory)
                    if x.endswith('json')
                    ]
        except FileNotFoundError as error:
            logger.error(f"Reading quiz directory: {error}")
            return []

    def _get_quiz_summaries_from_file_list(self, quiz_file_paths):
        def get_name_title_filename_from(quiz_filename):
            document = self._read_quiz_doc_from_file(quiz_filename)
            return document['name'], document['title'], quiz_filename

        return [get_name_title_filename_from(filename)
                for filename in quiz_file_paths]

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
        try:
            return self._read_quiz_doc_from_file(filename)
        except JSONDecodeError as err:
            logger.error(f"Not valid JSON: {filename}. {err}")
            return None
