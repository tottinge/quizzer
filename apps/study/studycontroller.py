from typing import NamedTuple, Iterable

from quizzes.question import Question
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizSummary
from sessions.session_id import create_session_id
from shared.quizzology import Quizzology


class StudyController:

    def __init__(self, quizzology: Quizzology):
        self.quizzology = quizzology

    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        return self.quizzology.quiz_store.get_quiz_summaries()

    def get_quiz_by_name(self, quiz_name: str) -> Quiz:
        return self.quizzology.quiz_store.get_quiz(quiz_name)

    @staticmethod
    def begin_session(http_response):
        create_session_id(http_response)

    def record_answer(self, session_id, quiz_name, question_number, selection,
                      correct, timestamp, question_id):
        self.quizzology.session_store.record_answer(
            session_id,
            quiz_name,
            question_number,
            selection,
            correct,
            question_id,
            timestamp
        )

    def number_of_incorrect_answers(self, session_id, quiz_name):
        session_store = self.quizzology.session_store
        return session_store.number_of_incorrect_answers(session_id, quiz_name)

    class PreparedQuestion(NamedTuple):
        quiz: Quiz
        question: Question
        question_number: int

    @staticmethod
    def prepare_quiz_question_document(quiz: Quiz,
                                       question_number=0) -> PreparedQuestion:
        selected_question = quiz.question_by_number(question_number) \
            if quiz.has_questions() \
            else Question.from_json({})
        return StudyController.PreparedQuestion(
            quiz=quiz,
            question=selected_question,
            question_number=question_number
        )

    def begin_quiz(self, quiz: Quiz) -> PreparedQuestion:
        return self.prepare_quiz_question_document(
            quiz,
            quiz.first_question_number()
        )

    def get_log_messages(self):
        return self.quizzology.session_store.get_all()

    class RecordedAnswer(NamedTuple):
        quiz: Quiz
        title: str
        question_number: int
        correct: bool
        confirmation: str
        selection: str
        incorrect_answers: int
        next_question_number: int
        session_id: str

        def quiz_is_finished(self):
            return (self.question_number == self.quiz.last_question_number()
                    and self.correct)

    def record_answer_and_get_status(self,
                                     question_number: int,
                                     quiz: Quiz,
                                     selection: str,
                                     session_id: str) -> RecordedAnswer:
        question = quiz.question_by_number(question_number)
        correct = question.is_correct_answer(selection)

        self.record_answer(session_id, quiz.name, question_number, selection,
                           correct, None, question.question_id)
        incorrect_answers = self.number_of_incorrect_answers(session_id,
                                                             quiz.name)
        next_question_number = quiz.next_question_number(question_number) \
            if correct \
            else None
        return StudyController.RecordedAnswer(
            quiz=quiz,
            title=quiz.title,
            question_number=question_number,
            correct=correct,
            confirmation=question.confirmation if correct else "",
            selection=selection,
            incorrect_answers=incorrect_answers,
            next_question_number=next_question_number,
            session_id=session_id
        )

    def get_log_message_for_question(self, session_id, quiz_name,
                                     question_number):
        return self.quizzology.session_store.get_log_message(
            session_id,
            quiz_name,
            question_number
        )
