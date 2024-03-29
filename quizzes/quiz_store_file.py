import json
import os
from dataclasses import asdict
from json import JSONDecodeError
from logging import getLogger
from typing import Iterable, Optional

from sanitize_filename import sanitize

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizSummary, SaveQuizResult

logger = getLogger(__name__)
defang_bad_chars = str.maketrans(
    {"~": "_", " ": "_", "&": "-n-", "|": "-r-", '"': "", "'": "", ";": ""}
)


class QuizStoreFile:
    """For consideration
    * why not do a dir walk?
    * instead of filename, an ID in summaries?
    """

    def __init__(self, dir_name="quiz_content"):
        self.quiz_dir = dir_name

    def __str__(self):
        return f"QuizStoreFile({self.quiz_dir})"

    def filename_for(self, name: str) -> str:
        existing = self._find_file_for_named_quiz(name)
        if existing:
            return existing
        new_filename = sanitize(name.translate(defang_bad_chars) + ".json")
        return os.path.join(self.quiz_dir, new_filename)

    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        file_list = self._get_quiz_files_from_directory(self.quiz_dir)
        return self._get_quiz_summaries_from_file_list(file_list)

    def get_quiz(self, quiz_name: str) -> Optional[Quiz]:
        filename = self._find_file_for_named_quiz(quiz_name)
        if not filename:
            return None
        document = self._read_quiz_document(filename)
        return Quiz.from_json(document) if document else None

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        filename = self.filename_for(quiz.name)
        try:
            self._dump_quiz_to(filename, quiz)
            return SaveQuizResult(
                id=filename, success=True, message=f"saved quiz to {filename}"
            )
        except OSError as error:
            return SaveQuizResult(id=filename, success=False, message=error.strerror)

    def _dump_quiz_to(self, filename, quiz):
        with open(filename, "w") as output:
            json.dump(asdict(quiz), output)

    def exists(self, quiz_name: str) -> bool:
        found_file_name = self._find_file_for_named_quiz(quiz_name)
        return found_file_name is not None

    # -- helper methods all the rest of the way down --------

    @staticmethod
    def _get_quiz_files_from_directory(directory: str) -> list:
        try:
            return [
                os.path.join(directory, x)
                for x in os.listdir(directory)
                if x.endswith("json")
            ]
        except FileNotFoundError as error:
            logger.error(f"Reading quiz directory: {error}")
            return []

    def _get_quiz_summaries_from_file_list(
        self, quiz_file_paths
    ) -> Iterable[QuizSummary]:
        for quiz_filename in quiz_file_paths:
            try:
                document = self._read_quiz_doc_from_file(quiz_filename)
                summary = QuizSummary(
                    name=document["name"],
                    title=document["title"],
                    id=quiz_filename,
                    image_url=document.get("image_url", "/favicon.ico"),
                )
                yield summary
            except json.JSONDecodeError as err:
                logger.error(f"FAILED: {quiz_filename}: {str(err)}")

    @staticmethod
    def _read_quiz_doc_from_file(filename):
        with open(filename) as input_file:
            return json.load(input_file)

    def _find_file_for_named_quiz(self, quiz_name: str) -> Optional[str]:
        lookup = {summary.name: summary.id for summary in self.get_quiz_summaries()}
        filename = lookup.get(quiz_name)
        return filename

    def _read_quiz_document(self, filename: str) -> Optional[dict]:
        try:
            return self._read_quiz_doc_from_file(filename)
        except JSONDecodeError as err:
            message = f"Not valid JSON: {filename}. {err}"
            logger.error(message)
            return None
        except OSError as err:
            logger.error("Cannot read %s, '%s'", filename, err)
