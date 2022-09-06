import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

import apps
import main
import security.authn
from apps.study.session_store import SessionStore
from apps.study.study import render_judgment, url_for, use_this_quizzology
from quizzes.question import Question
from quizzes.quiz import Quiz
from security import authz
from shared.quizzology import Quizzology
from shared.user import User


class TestSession(unittest.TestCase):
    def setUp(self):
        use_this_quizzology(self.context_with_in_memory_session_store())

        self.question = Question(
            text='whatever',
            decoys=['falsehood', 'foolishness'],
            answer='the truth',
            confirmation="confirmation text"
        )
        self.quiz = Quiz(
            title='frankfurter',
            name='TestSessionQuiz',
            questions=[self.question]
        )

    def context_with_in_memory_session_store(self):
        return Quizzology(session_store=(
            SessionStore(TinyDB(storage=MemoryStorage))))

    def test_answer_appears_in_session_page(self):
        session_id = "id"
        name = "quiz_name"
        question = 222
        user_answer = "selection"
        correct = True
        question_id = "fa2f84f1-cf9e-4307-878b-c17af8d02c18"
        timestamp = "TODAY"
        study_controller = apps.study.study.study_controller
        study_controller.record_answer(session_id, name, question, user_answer,
                                       correct, timestamp, question_id)

        with self.authorization_as('author', 'test'):
            result = main.show_session()

            self.assertIn(session_id, result)
            self.assertIn(name, result)
            self.assertIn(str(question), result)
            self.assertIn(user_answer, result)
            self.assertIn(str(correct), result)
            self.assertIn(timestamp, result)

    def authorization_as(self, role, user_name):
        user = User(user_name=user_name, role=role, password_hash="")
        token = security.authn.make_bearer_token(user)
        patch_object = patch.object(authz, 'get_authorization_token',
                                    return_value=token)
        return patch_object

    def test_render_judgment_incorrect_answer(self):
        markup = render_judgment(self.quiz, 0, "")
        doc = BeautifulSoup(markup, "html.parser")

        clean_text = ' '.join(doc.text.split())
        self.assertIn("not what we're looking for", clean_text)
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
        confirmation_tag = doc.body.find("div", id="confirm_correct")
        self.assertIn(self.question.confirmation, confirmation_tag.text)

    def test_offers_next_question_if_any_exist(self):
        second_question = Question(
            text="Second",
            decoys=[],
            answer="answer"
        )
        quiz = Quiz(
            title='2q',
            name='Test2Questions',
            questions=[self.question, second_question]
        )

        markup = render_judgment(quiz, 0, "the truth")
        doc = BeautifulSoup(markup, "html.parser")
        next_page_anchor = doc.body.find("a", id="next_question")

        self.assertIsNotNone(next_page_anchor,
                             "Should have next_question link.")

        expected_question_number = quiz.next_question_number(0)
        expected_url = url_for(quiz, expected_question_number)
        self.assertEqual(expected_url, next_page_anchor['href'])

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
