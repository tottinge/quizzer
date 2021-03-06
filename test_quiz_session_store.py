import unittest

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from session_store import SessionStore


class SessionStoreStuff(unittest.TestCase):

    def setUp(self):
        self.session_store = SessionStore(TinyDB(storage=MemoryStorage))

    def test_record_correct_answer(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_id = 'test_' + session_store.get_new_session_id()

        session_store.record_answer(session_id, quiz_name, 10, 'selection', True)

        [record] = session_store.perfect_answers(session_id, quiz_name)
        self.assertTrue(record.is_correct)
        self.assertEqual(session_id, record.session_id)
        self.assertEqual(quiz_name, record.quiz_name)
        correct = session_store.number_of_correct_answers(session_id, quiz_name)
        self.assertEqual(1, correct)
        incorrect = session_store.number_of_incorrect_answers(session_id, quiz_name)
        self.assertEqual(0, incorrect)

    def test_record_incorrect_answer(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_id = 'test_' + session_store.get_new_session_id()

        session_store.record_answer(session_id, quiz_name, 0, 'selection', False)

        self.assertEqual(0, session_store.number_of_correct_answers(session_id, quiz_name))
        self.assertEqual(1, session_store.number_of_incorrect_answers(session_id, quiz_name))
        [record] = session_store.incorrect_answers(session_id, quiz_name)
        self.assertEqual(session_id, record.session_id)
        self.assertEqual(quiz_name, record.quiz_name)
        self.assertEqual(False, record.is_correct)

    def test_get_new_session_id(self):
        session_store = self.session_store
        self.assertIsNotNone(session_store.get_new_session_id())

    def test_recorded_answers_are_unique_within_session(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_1 = "test_" + session_store.get_new_session_id()
        session_2 = "test_" + session_store.get_new_session_id()

        session_store.record_answer(session_1, quiz_name, 10, "selection", True)
        session_store.record_answer(session_1, quiz_name, 10, "selection", False)
        session_store.record_answer(session_2, quiz_name, 10, "selection", True)
        session_store.record_answer(session_2, quiz_name, 10, "selection", True)

        self.assertEqual(1, session_store.number_of_correct_answers(session_1, quiz_name))
        self.assertEqual(1, session_store.number_of_incorrect_answers(session_1, quiz_name))
        self.assertEqual(2, session_store.number_of_correct_answers(session_2, quiz_name))
        self.assertEqual(0, session_store.number_of_incorrect_answers(session_2, quiz_name))

    def test_questions_answered_correctly_coalesces(self):
        session_store = self.session_store
        session_id = 'session'
        inputs = [
            (session_id, 'quiz', 1, '', True),
            (session_id, 'quiz', 1, '', True),
            (session_id, 'quiz', 2, '', False),
        ]
        for each in inputs:
            session_store.record_answer(*each)
        actual = session_store.questions_answered_correctly(session_id)

        self.assertEqual(1, len(actual))
        self.assertIn(('quiz', 1), actual)

    def test_questions_answered_incorrectly_coalesces(self):
        session_store = self.session_store
        session_id = 'session'
        inputs = [
            (session_id, 'quiz', 1, '', False),
            (session_id, 'quiz', 1, '', False),
            (session_id, 'quiz', 1, '', True),
            (session_id, 'quiz', 2, '', True),
        ]
        for each in inputs:
            session_store.record_answer(*each)
        actual = session_store.questions_answered_incorrectly(session_id)

        self.assertEqual(1, len(actual))
        self.assertIn(('quiz', 1), actual)
        self.assertNotIn(('quiz', 2), actual)


if __name__ == '__main__':
    unittest.main()
