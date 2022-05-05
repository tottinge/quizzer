from typing import Optional

from quizzes.quiz import Quiz
from quizzes.quiz_store import SaveQuizResult
from shared.quizzology import Quizzology


class AuthorController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology

    def save(self, quiz: Quiz) -> SaveQuizResult:
        return self.quizzology.quiz_store.save_quiz(quiz)

    def quiz_exists(self, quiz_name: str) -> bool:
        return self.quizzology.quiz_store.exists(quiz_name)

    def get_quiz(self, quiz_name: str) -> Optional[Quiz]:
        return self.quizzology.quiz_store.get_quiz(quiz_name)
