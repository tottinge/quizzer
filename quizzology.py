from question import Question
from quiz import Quiz
from quiz_store import QuizStore
from session_store import SessionStore

SESSION_COOKIE_ID = "qz_current_quiz"


class Quizzology:
    quiz_store = None
    session_store = None

    def set_quiz_store(self, new_store: QuizStore):
        self.quiz_store = new_store

    def get_quiz_store(self) -> QuizStore:
        return self.quiz_store

    def set_session_store(self, session_store: SessionStore):
        self.session_store = session_store

    def get_session_store(self) -> SessionStore:
        return self.session_store

    def get_quiz_summaries(self) -> list:
        return self.quiz_store.get_quiz_summaries()

    def get_quiz_by_name(self, quiz_name: str) -> Quiz:
        return self.quiz_store.get_quiz(quiz_name)

    @staticmethod
    def begin_session(http_response):
        http_response.delete_cookie(SESSION_COOKIE_ID)

    def record_answer(self, session_id, quiz_name, question_number, selection,
                      correct, timestamp):
        self.get_session_store().record_answer(session_id, quiz_name,
                                               question_number,
                                               selection,
                                               correct,
                                               timestamp)

    def number_of_incorrect_answers(self, quiz_name, session_id):
        return self.get_session_store().number_of_incorrect_answers(
            session_id,
            quiz_name)

    @staticmethod
    def prepare_quiz_question_document(quiz, question_number=0):
        selected_question = quiz.question_by_number(question_number) \
            if quiz.has_questions() \
            else Question.from_json({})
        return dict(
            quiz=quiz,
            question=selected_question,
            question_number=question_number
        )

    def begin_quiz(self, quiz: Quiz) -> dict:
        return self.prepare_quiz_question_document(quiz, 0)

    def new_session_id(self):
        return self.session_store.get_new_session_id()

    def get_log_messages(self):
        return self.session_store.get_all()
