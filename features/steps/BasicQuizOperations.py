import json
import os

from behave import *
# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from behave.runner import Context
from hamcrest import assert_that, equal_to, not_none
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from quizzes.question import Question
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology
from sessions.session_store import SessionStore, AnswerEntry


@given("a student starts quizzology")
def step_impl(context: Context):
    quizzology: Quizzology = Quizzology()
    assert quizzology is not None
    quizzology.set_quiz_store(QuizStore(context.temporary_directory.name))
    session_store = SessionStore(TinyDB(storage=MemoryStorage))
    quizzology.set_session_store(session_store)
    context.quizzology = quizzology


@step('we have a quiz called "{quiz_name}"')
def step_impl(context: Context, quiz_name: str):
    questions = [
        Question(question=f"{quiz_name}'s first", answer="?", decoys=[])]
    quiz = Quiz(
        title=f"This is {quiz_name}",
        name=quiz_name,
        questions=questions
    )
    save_quiz(context, quiz)


@given('we have a quiz called "{quiz_name}" with questions')
def step_impl(context: Context, quiz_name: str):
    questions = [Question(question=row["question"],
                          answer=row["answer"],
                          decoys=[])
                 for row in context.table]
    quiz = Quiz(title=quiz_name, name=quiz_name, questions=questions)
    save_quiz(context, quiz)


@step('the student selects the quiz called "{quiz_name}"')
def step_impl(context: Context, quiz_name: str):
    quizzology = context.quizzology
    quiz = quizzology.get_quiz_by_name(quiz_name)
    context.current_question = quizzology.begin_quiz(quiz)
    assert_that(context.current_question.quiz, equal_to(quiz))


@then('the "{quiz_name}" quiz is in-progress')
def step_impl(context: Context, quiz_name: str):
    # Dictionary for selecting cats quiz contains cats quiz
    first_question = context.current_question
    assert (
            first_question is not None
            and first_question["quiz"].name == quiz_name
    )
    assert_that(first_question, not_none())
    assert_that(first_question["quiz"].name, equal_to(quiz_name))


@step('the first "{quiz_name}" question is displayed')
def step_impl(context: Context, quiz_name: str):
    current_question = context.current_question
    assert_that(current_question.quiz.name, equal_to(quiz_name))

    expected_first_question = current_question.quiz.first_question()
    actual_first_question = current_question.question
    assert_that(actual_first_question, equal_to(expected_first_question))


def save_quiz(context: Context, quiz: Quiz):
    """
    This is done in the test helpers because authoring is not a feature
    of quizzology so far. When there is a proper authoring system, we will
    want to use its features rather than a test helper, so that we stop
    being data-structure-aware here.
    """
    dir_name = context.temporary_directory.name
    filename = os.path.join(dir_name, quiz.name + ".json")
    with open(filename, "w") as output:
        json.dump(quiz.to_dict(), output)


@when('the student answers "{answer}"')
def step_impl(context: Context, answer: str):
    context.recent_answer = context.quizzology.record_answer_and_get_status(
        question_number=context.current_question.question_number,
        quiz=context.current_question.quiz,
        selection=answer,
        session_id=None)


@then("the answer is confirmed as correct")
def step_impl(context: Context):
    assert_that(context.recent_answer.correct, f"Answer should be correct")


@step('the next question is "{question_text}"')
def step_impl(context: Context, question_text: str):
    quiz: Quiz = context.recent_answer.quiz
    next_question_number: int = context.recent_answer.next_question_number
    question: Question = quiz.question_by_number(next_question_number)
    assert_that(question.question, equal_to(question_text))


@step("the log shows the question was answered {how}")
def step_impl(context: Context, how: str):
    quizzology: Quizzology = context.quizzology
    session_id = context.recent_answer.session_id
    quiz_name = context.recent_answer.quiz.name
    question_number = context.recent_answer.question_number
    log: AnswerEntry = quizzology.get_log_message_for_question(session_id, quiz_name, 
                                                               question_number)
    user_choice = log.selection
    expected = (how == "correctly")
    assert_that(log.is_correct, equal_to(expected),
                f"User said '{user_choice}', which is answered {how}")
