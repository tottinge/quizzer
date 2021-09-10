from quizzes.quiz import Quiz
from shared.quizzology import Quizzology


class AuthorController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology