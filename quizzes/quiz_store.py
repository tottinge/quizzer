import json
import os
import typing
from dataclasses import asdict
from json import JSONDecodeError
from logging import getLogger
from typing import Optional, NamedTuple

from sanitize_filename import sanitize

from quizzes.quiz import Quiz

logger = getLogger(__name__)


def filename_for(name):
    return sanitize(name.replace('~', '-').replace(' ', '_') + '.json')


class QuizStore:
    """ For consideration
    * why not do a dir walk?
    * instead of filename, an ID in summaries?
    """

    def __init__(self, dir_name='quiz_content'):
        self.quiz_dir = dir_name

    def get_quiz_summaries(self) -> typing.Iterable:
        file_list = self._get_quiz_files_from_directory(self.quiz_dir)
        return self._get_quiz_summaries_from_file_list(file_list)

    def get_quiz(self, quiz_name: str) -> Optional[Quiz]:
        filename = self._find_file_for_named_quiz(quiz_name)
        document = self._read_quiz_document(filename)
        return Quiz.from_json(document) if document else None

    class SaveQuizResult(NamedTuple):
        id: str
        success: bool
        message: str

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        dir_name = self.quiz_dir
        file_name = filename_for(quiz.name)
        filename = os.path.join(dir_name, file_name + ".json")
        try:
            with open(filename, "w") as output:
                json.dump(asdict(quiz), output)
            return QuizStore.SaveQuizResult(
                id=filename,
                success=True,
                message=f'saved quiz to {filename}'
            )
        except OSError as error:
            return QuizStore.SaveQuizResult(
                id=filename,
                success=False,
                message=error.strerror
            )

    @staticmethod
    def shutdown():
        logger.critical("quiz_store shutting down")

    # -- helper methods all the rest of the way down --------

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

    def _get_quiz_summaries_from_file_list(self,
                                           quiz_file_paths) -> typing.Iterable:
        for quiz_filename in quiz_file_paths:
            try:
                document = self._read_quiz_doc_from_file(quiz_filename)
                yield document['name'], document['title'], quiz_filename
            except json.JSONDecodeError as err:
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

    def _read_quiz_document(self, filename: str) -> Optional[dict]:
        try:
            return self._read_quiz_doc_from_file(filename)
        except JSONDecodeError as err:
            logger.error(f"Not valid JSON: {filename}. {err}")
            return None
