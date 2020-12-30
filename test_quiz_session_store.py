import unittest

from session_store import SessionStore


class SessionStoreStuff(unittest.TestCase):
    
    def test_record_correct_answer(self):
        session_store = SessionStore()
        quiz_name = "quiz_name"
        session_store.record_answer(quiz_name, 0, "selection", True)
        self.assertEqual(1, session_store.number_of_correct_answers(quiz_name))
        self.assertEqual([(quiz_name, 0, 'selection', True)], session_store.perfect_answers(quiz_name))
        self.assertEqual(0, session_store.number_of_incorrect_answers(quiz_name))

    def test_record_incorrect_answer(self):
        session_store = SessionStore()
        quiz_name = "quiz_name"
        session_store.record_answer(quiz_name, 0, "selection", False)
        self.assertEqual(0, session_store.number_of_correct_answers(quiz_name))
        self.assertEqual(1, session_store.number_of_incorrect_answers(quiz_name))
        self.assertEqual([(quiz_name, 0, 'selection', False)], session_store.incorrect_answers(quiz_name))



if __name__ == '__main__':
    unittest.main()
