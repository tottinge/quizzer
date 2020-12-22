import unittest
from unittest.mock import patch

from box import Box
from bs4 import BeautifulSoup

from main import is_answer_correct, check_answer, render_judgment
from quiz_store import Quiz


class TestSession(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

        self.question = Box({
            'question': 'whatever',
            'answer': 'the truth',
            'decoys': ['falsehood', 'foolishness']
        })
        self.quiz = Quiz({
            'title':'frankfurter',
            'name':'TestSessionQuiz',
            'questions': [self.question]
        })

    def test_answer_question_correctly(self):
        result = is_answer_correct(self.question, self.question["answer"])
        self.assertTrue(
            result,
            "Rejected correct answer 'the truth'")

    def test_answer_question_incorrectly(self):
        result = is_answer_correct(self.question, "falsehood")
        self.assertFalse(
            result,
            f"Accepted 'falsehood' where answer is {self.question['answer']}"
        )

    def test_render_judgment_incorrect_answer(self):
        markup = render_judgment(self.quiz, 0, "")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIn("not what we're looking for", doc.text)
        self.assertIsNotNone(doc.body.find("a", id="try_again"), "Should be a try_again link")

    def test_render_judgment_correct_answer(self):
        markup = render_judgment(self.quiz, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIn("is correct", doc.text)
        self.assertIsNone(doc.body.find("a", id="try_again"), "Should have no try_again link when correct answer given.")

    def test_no_next_url_offered_if_no_more_questions_exist(self):
        markup = render_judgment(self.quiz, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIsNone(doc.body.find("a", id="next_question"), "Should have no next_question link (only 1 question).")


    def test_offers_next_question_if_any_exist(self):
        two_question = Quiz({
            'title':'2q',
            'name':'Test2Questions',
            'questions': [self.question, self.question]
        })
        markup = render_judgment(two_question, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIsNotNone(doc.body.find("a", id="next_question"), "Should have next_question link.")
