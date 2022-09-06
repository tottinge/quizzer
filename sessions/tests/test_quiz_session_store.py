import unittest

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from apps.study.session_store import SessionStore


class SessionStoreStuff(unittest.TestCase):

    def setUp(self):
        self.session_store = SessionStore(TinyDB(storage=MemoryStorage))

    def test_record_correct_answer(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_id = 'test_session'

        session_store.record_answer(session_id, quiz_name, 10, 'selection',
                                    True, "")

        [record] = session_store.perfect_answers(session_id, quiz_name)
        self.assertTrue(record.is_correct)
        self.assertEqual(session_id, record.session_id)
        self.assertEqual(quiz_name, record.quiz_name)
        correct = session_store.number_of_correct_answers(session_id,
                                                          quiz_name)
        self.assertEqual(1, correct)
        incorrect = session_store.number_of_incorrect_answers(session_id,
                                                              quiz_name)
        self.assertEqual(0, incorrect)

    def test_record_incorrect_answer(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_id = 'test_session'

        session_store.record_answer(session_id, quiz_name, 0, 'selection',
                                    False, "")

        self.assertEqual(0, session_store.number_of_correct_answers(session_id,
                                                                    quiz_name))
        self.assertEqual(1,
                         session_store.number_of_incorrect_answers(session_id,
                                                                   quiz_name))
        [record] = session_store.incorrect_answers(session_id, quiz_name)
        self.assertEqual(session_id, record.session_id)
        self.assertEqual(quiz_name, record.quiz_name)
        self.assertEqual(False, record.is_correct)

    def test_recorded_answers_are_unique_within_session(self):
        session_store = self.session_store
        quiz_name = "quiz_name"
        session_1 = "test_session_1"
        session_2 = "test_session_2"

        inputs = [
            (session_1, quiz_name, 10, "selection", True, "82ee1cce-c070-416f-b20a-1e8b8d5b225e"),
            (session_1, quiz_name, 10, "selection", False, "da8db82a-bcf3-4b7f-a24d-317779d2f4f3"),
            (session_2, quiz_name, 10, "selection", True, "9feadac9-461a-4971-9fc5-c29c71bef400"),
            (session_2, quiz_name, 10, "selection", True, "31c01cee-9ccf-4862-88bf-287d3a41374e")
        ]
        for record in inputs:
            session_store.record_answer(*record)

        correct_answers_for = session_store.number_of_correct_answers
        incorrect_answers_for = session_store.number_of_incorrect_answers

        self.assertEqual(1, correct_answers_for(session_1, quiz_name))
        self.assertEqual(1, incorrect_answers_for(session_1, quiz_name))

        self.assertEqual(2, correct_answers_for(session_2, quiz_name))
        self.assertEqual(0, incorrect_answers_for(session_2, quiz_name))

    def test_questions_answered_correctly_coalesces(self):
        session_store = self.session_store
        session_id = 'session'
        inputs = [
            (session_id, 'quiz', 1, '', True, 'e7324052-724b-43b3-a97b-ba09f6ed635c'),
            (session_id, 'quiz', 1, '', True, 'e3bab1ed-6aa8-47f6-b305-9a63bdd93bb1'),
            (session_id, 'quiz', 2, '', False, '12839d3a-42d3-41e2-ae89-9ed6a943aa6e'),
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
            (session_id, 'quiz', 1, '', False, '47769af3-3596-4c2c-b879-075c9e9acf9f'),
            (session_id, 'quiz', 1, '', False, 'e878bde5-d973-4786-a758-ce021cdca0d1'),
            (session_id, 'quiz', 1, '', True, '8b71a148-b280-4e3d-a0f7-a607067e7d87'),
            (session_id, 'quiz', 2, '', True, 'eeb1ac27-43e1-4f43-ba25-ac876f7268ff'),
        ]
        for each in inputs:
            session_store.record_answer(*each)
        actual = session_store.questions_answered_incorrectly(session_id)

        self.assertEqual(1, len(actual))
        self.assertIn(('quiz', 1), actual)
        self.assertNotIn(('quiz', 2), actual)


if __name__ == '__main__':
    unittest.main()
