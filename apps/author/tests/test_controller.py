import unittest

from apps.author import author_controller


class MyTestCase(unittest.TestCase):
    def create_new_quiz(self):
        new_quiz = author_controller.create_new_quiz(
            name='testcreation',
            title="test"
        )


if __name__ == '__main__':
    unittest.main()
