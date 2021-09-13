from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class AuthorController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology

    def save(self, quiz) -> bool:
        result = self.quizzology.quiz_store.save_quiz(quiz)
        return result.success

    def quiz_exists(self, quiz_name):
        store: QuizStore = self.quizzology.quiz_store
        return store.exists(quiz_name)