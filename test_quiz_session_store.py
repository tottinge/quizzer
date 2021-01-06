import unittest

from session_store import SessionStore


class SessionStoreStuff(unittest.TestCase):
    
    def test_record_correct_answer(self):
        session_store = SessionStore()
        quiz_name = "quiz_name"
        session_id = session_store.get_new_session_id()
        expected_record = (session_id, quiz_name, 0, 'selection', True)

        session_store.record_answer(*expected_record)

        self.assertEqual(1, session_store.number_of_correct_answers(session_id, quiz_name))
        self.assertEqual([expected_record], session_store.perfect_answers(session_id, quiz_name))
        self.assertEqual(0, session_store.number_of_incorrect_answers(session_id, quiz_name))

    def test_record_incorrect_answer(self):
        session_store = SessionStore()
        quiz_name = "quiz_name"
        session_id = session_store.get_new_session_id()
        expected_record = (session_id, quiz_name, 0, 'selection', False)

        session_store.record_answer(*expected_record)

        self.assertEqual(0, session_store.number_of_correct_answers(session_id, quiz_name))
        self.assertEqual(1, session_store.number_of_incorrect_answers(session_id, quiz_name))
        self.assertEqual([expected_record], session_store.incorrect_answers(session_id, quiz_name))

    def test_get_new_session_id(self):
        session_store = SessionStore()
        self.assertIsNotNone(session_store.get_new_session_id())

    def test_recorded_answers_are_unique_within_session(self):
        session_store = SessionStore()
        quiz_name = "quiz_name"
        session_1 = session_store.get_new_session_id()
        session_2 = session_store.get_new_session_id()

        session_store.record_answer(session_1, quiz_name, 10, "selection", True)
        session_store.record_answer(session_1, quiz_name, 10, "selection", False)
        session_store.record_answer(session_2, quiz_name, 10, "selection", True)
        session_store.record_answer(session_2, quiz_name, 10, "selection", True)

        self.assertEqual(1, session_store.number_of_correct_answers(session_1, quiz_name))
        self.assertEqual(1, session_store.number_of_incorrect_answers(session_1, quiz_name))
        self.assertEqual(2, session_store.number_of_correct_answers(session_2, quiz_name))
        self.assertEqual(0, session_store.number_of_incorrect_answers(session_2, quiz_name))



if __name__ == '__main__':
    unittest.main()
