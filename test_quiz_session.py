import unittest
from unittest.mock import patch

from main import is_answer_correct, check_answer, render_judgment


class TestSession(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.question = {
            "question": "whatever",
            "answer": "the truth",
            "decoys": ["falsehood", "foolishness"]
        }

    def test_answer_question_correctly(self):
        actual = is_answer_correct(
            self.question,
            self.question["answer"]
        )
        self.assertTrue(actual, "Rejected correct answer 'the truth'")

    def test_answer_question_incorrectly(self):
        self.assertFalse(
            is_answer_correct(self.question, "falsehood"),
            f"Accepted 'falsehood' where answer is {self.question['answer']}"
        )

    def test_render_judgment(self):
        render_judgment(self.question, "")