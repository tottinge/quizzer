import unittest

from bottle import LocalRequest, LocalResponse
from bs4 import BeautifulSoup
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

import main
from main import (
    render_judgment,
    get_client_session_id,
    SESSION_COOKIE_ID,
    drop_client_session_id
)
from quiz import Quiz, Question
from session_store import SessionStore


class TestSession(unittest.TestCase):
    def setUp(self):
        main.quizzology.set_session_store(
            SessionStore(TinyDB(storage=MemoryStorage)))
        self.question = dict(
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
        main.quizzology.get_session_store().record_answer(
            session_id, name, question, user_answer, correct, timestamp
        )
        result = main.show_session()
        self.assertIn(session_id, result)
        self.assertIn(name, result)
        self.assertIn(str(question), result)
        self.assertIn(user_answer, result)
        self.assertIn(str(correct), result)
        self.assertIn(timestamp, result)

    def test_answer_question_correctly(self):
        q = Question(**self.question)
        self.assertTrue(
            q.is_correct_answer(q.answer),
            f"Rejected correct answer '{q.answer}'")

    def test_answer_question_incorrectly(self):
        q = Question(**self.question)
        self.assertFalse(
            q.is_correct_answer("falsehood"),
            f"Accepted 'falsehood' where answer is {q.answer}"
        )

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


class TestSessionCookieHandling(unittest.TestCase):

    @staticmethod
    def fresh_session_objects():
        return LocalRequest(), LocalResponse()

    @staticmethod
    def cookies_from_response(response):
        """Extract cookies into a dictionary from the response
        without violating encapsulation"""
        entries = [value.split(';')[0] for (key, value) in response.headerlist
                   if key == 'Set-Cookie']
        return dict((value.split('=', 1)) for value in entries)

    def get_session_cookie(self, response):
        cookies = self.cookies_from_response(response)
        session_cookie_id = cookies.get(SESSION_COOKIE_ID)
        return session_cookie_id

    def test_create_session_cookie(self):
        request, response = self.fresh_session_objects()

        session_id = get_client_session_id(request, response)

        self.assertIsNotNone(
            session_id,
            "Cookies should be created when needed"
        )
        self.assertIsNotNone(
            self.get_session_cookie(response),
            "Cookies should be set in the response object"
        )

    def test_retains_session_cookie(self):
        request, response = self.fresh_session_objects()
        request.cookies[SESSION_COOKIE_ID] = "ImFake"

        session_id = get_client_session_id(request, response)

        self.assertEqual("ImFake", session_id)

    def test_can_drop_session_cookie(self):
        """
        Surprisingly, deleting a cookie doesn't remove the Set-Cookie
        header for a value. It merely changes it to a string of double-quotes.
        The header is *asking* the browser to set the cookie to "".
        The real activity takes place on the browser.
        """
        request, response = self.fresh_session_objects()
        old_id = get_client_session_id(request, response)
        drop_client_session_id(response)
        self.assertNotEqual(old_id, self.get_session_cookie(response))
