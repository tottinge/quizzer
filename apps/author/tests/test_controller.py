import unittest

from apps.author.author_controller import AuthorController
from shared.quizzology import Quizzology


class MyTestCase(unittest.TestCase):
    def create_new_quiz(self):
        quizzology = Quizzology()
        x = AuthorController(quizzology)
        pass


if __name__ == '__main__':
    unittest.main()
