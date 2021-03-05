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

    def get_quiz_summaries(self) -> list:
        file_list = self._get_quiz_files_from_directory(self.quiz_dir)
        return self._get_quiz_summaries_from_file_list(file_list)

    def get_quiz(self, quiz_name: str):
        filename = self._find_file_for_named_quiz(quiz_name)
        document = self._read_quiz_document(filename)
        return Quiz.from_json(document) if document else None

    @staticmethod
    def _get_quiz_files_from_directory(directory: str) -> list:
        try:
            return [os.path.join(directory, x)
                    for x in os.listdir(directory)
                    if x.endswith('json')
                    ]
        except FileNotFoundError as error:
            logger.error(f"Reading quiz directory: {error}")
            return []

    def _get_quiz_summaries_from_file_list(self, quiz_file_paths) -> list:
        for quiz_filename in quiz_file_paths:
            try:
                document = self._read_quiz_doc_from_file(quiz_filename)
                yield document['name'], document['title'], quiz_filename
            except Exception as err:
                logger.error(f"FAILED: {quiz_filename}: {str(err)}")

    @staticmethod
    def _read_quiz_doc_from_file(filename):
        with open(filename) as input_file:
            return json.load(input_file)

    def _find_file_for_named_quiz(self, quiz_name: str) -> str:
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
