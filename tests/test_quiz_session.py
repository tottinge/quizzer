import unittest

from bs4 import BeautifulSoup
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

import main
from main import (
    render_judgment
)
from quizzes.question import Question
from quizzes.quiz import Quiz
from sessions.session_store import SessionStore


class TestSession(unittest.TestCase):
    def setUp(self):
        main.quizzology.set_session_store(
            SessionStore(TinyDB(storage=MemoryStorage)))
        self.question = Question(
            question='whatever',
            answer='the truth',
            decoys=['falsehood', 'foolishness']
        )
        self.quiz = Quiz(
            title='frankfurter',
            name='TestSessionQuiz',
            questions=[self.question]
        )

    def test_answer_appears_in_session_page(self):
        session_id = "id"
        name = "quiz_name"
        question = 222
        user_answer = "selection"
        correct = True
        timestamp = "TODAY"
        main.quizzology.record_answer(session_id, name, question, user_answer,
                                      correct, timestamp)
        result = main.show_session()
        self.assertIn(session_id, result)
        self.assertIn(name, result)
        self.assertIn(str(question), result)
        self.assertIn(user_answer, result)
        self.assertIn(str(correct), result)
        self.assertIn(timestamp, result)


    def test_render_judgment_incorrect_answer(self):
        markup = render_judgment(self.quiz, 0, "")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIn("not what we're looking for", doc.text)
        self.assertIsNotNone(doc.body.find("a", id="try_again"),
                             "Should be a try_again link")

    def test_render_judgment_correct_answer(self):
        markup = render_judgment(self.quiz, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIn("is correct", doc.text)
        self.assertIsNone(
            doc.body.find("a", id="try_again"),
            "Should have no try_again link when correct answer given."
        )

    def test_offers_next_question_if_any_exist(self):
        two_question = Quiz(
            title='2q',
            name='Test2Questions',
            questions=[self.question, self.question]
        )
        markup = render_judgment(two_question, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIsNotNone(doc.body.find("a", id="next_question"),
                             "Should have next_question link.")

    def test_no_next_url_offered_if_no_more_questions_exist(self):
        markup = render_judgment(self.quiz, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        self.assertIsNone(
            doc.body.find("a", id="next_question"),
            "Should have no next_question link (only 1 question)."
        )
        self.assertIsNotNone(
            doc.body.find("a", id="go_home"),
            "Should be able to return to home page"
        )
