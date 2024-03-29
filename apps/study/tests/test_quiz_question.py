import unittest

from quizzes.question import Question


class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.question = Question(text='whatever',
                                 decoys=['falsehood', 'foolishness'],
                                 answer='the truth')

    def test_answer_question_correctly(self):
        self.assertTrue(
            self.question.is_correct_answer(self.question.answer),
            f"Rejected correct answer '{self.question.answer}'")

    def test_answer_question_incorrectly(self):
        negation = f"absolutely not {self.question.answer}"
        self.assertFalse(
            self.question.is_correct_answer(negation),
            f"Accepted '{negation}' where answer is {self.question.answer}"
        )
