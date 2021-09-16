from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class AuthorController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology

    def save(self, quiz) -> QuizStore.SaveQuizResult:
        return self.quizzology.quiz_store.save_quiz(quiz)

    def quiz_exists(self, quiz_name) -> bool:
        return self.quizzology.quiz_store.exists(quiz_name)
