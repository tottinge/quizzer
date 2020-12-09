import unittest
from unittest.mock import patch

from main import answer_question


class TestSession(unittest.TestCase):
    def test_answer_question_correctly(self):
        test_question = {
            "questions": [
                {
                    "question": "whatever",
                    "answer": "the truth",
                    "decoys": ["falsehood", "foolishness"]
                }
            ]
        }
        with patch('main.QUIZ_STORE.get_quiz') as getterMock:
            getterMock.return_value = test_question
            actual = answer_question("quiz_name", 0, "the truth")
            self.assertTrue(actual, "Rejected correct answer 'the truth'")

    def test_answer_question_incorrectly(self):
        test_question = {
            "questions": [
                {
                    "question": "whatever",
                    "answer": "the truth",
                    "decoys": ["falsehood", "foolishness"]
                }
            ]
        }
        with patch('main.QUIZ_STORE.get_quiz') as getterMock:
            getterMock.return_value = test_question
            self.assertFalse(answer_question("quiz_name", 0, "falsehood"),
                             "Accepted 'falsehood' where answer is 'the truth'")