from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class AuthorController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology

    def save(self, quiz: Quiz) -> QuizStore.SaveQuizResult:
        return self.quizzology.quiz_store.save_quiz(quiz)

    def quiz_exists(self, quiz_name: str) -> bool:
        return self.quizzology.quiz_store.exists(quiz_name)

    def get_quiz(self, quiz_name: str) -> Quiz:
        return self.quizzology.quiz_store.get_quiz(quiz_name)

