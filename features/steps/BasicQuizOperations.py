from behave import (given, when, then, step)
# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from behave.runner import Context
from hamcrest import assert_that, equal_to, not_none, is_not, empty, none, is_
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from apps.author.author_controller import AuthorController
from apps.study.studycontroller import StudyController
from quizzes.question import Question
from quizzes.quiz import Quiz
from quizzes.quiz_store_file import QuizStoreFile
from apps.study.session_store import AnswerEntry
from apps.study.session_store_tinydb import SessionStoreTinyDB
from shared.quizzology import Quizzology


@given("quizzology is running")
def step_impl_quizzology_is_running(context: Context):
    session_store = SessionStoreTinyDB(TinyDB(storage=MemoryStorage))
    quiz_store = QuizStoreFile(context.temporary_directory.name)
    quizzology = Quizzology(quiz_store, session_store)

    study_controller: StudyController = StudyController(quizzology)
    context.study_controller = study_controller

    author_controller: AuthorController = AuthorController(quizzology)
    context.author_controller = author_controller


@step('we have a quiz called "{quiz_name}"')
def step_impl_we_have_a_quiz(context: Context, quiz_name: str):
    questions = [
        Question(text=f"{quiz_name}'s first", decoys=[], answer="?")]
    quiz = Quiz(
        title=f"This is {quiz_name}",
        name=quiz_name,
        questions=questions
    )
    save_quiz(context, quiz)


@given('we have a quiz called "{quiz_name}" with questions')
def step_impl_we_have_quiz_with_questions(context: Context, quiz_name: str):
    questions = [Question(text=row["text"],
                          answer=row["answer"],
                          confirmation=row.get("confirmation", ""),
                          decoys=[])
                 for row in context.table]
    quiz = Quiz(title=quiz_name, name=quiz_name, questions=questions)
    save_quiz(context, quiz)


def current_question(context: Context) -> StudyController.PreparedQuestion:
    """
    Establishes the type of the current_question object to aid the
    IDE
    """
    return context.current_question


@step('the student selects the quiz called "{quiz_name}"')
def step_impl_student_selects_quiz_by_name(context: Context, quiz_name: str):
    study_controller: StudyController = context.study_controller
    quiz = study_controller.get_quiz_by_name(quiz_name)
    context.current_question = study_controller.begin_quiz(quiz)
    assert_that(context.current_question.quiz, equal_to(quiz))


@then('the "{quiz_name}" quiz is in-progress')
def step_impl_quiz_is_in_progress(context: Context, quiz_name: str):
    first_question = current_question(context)
    assert_that(first_question, not_none())
    assert_that(first_question.quiz.name, equal_to(quiz_name))


@step('the first "{quiz_name}" question is displayed')
def step_impl_first_question_is_displayed(context: Context, quiz_name: str):
    question = current_question(context)
    assert_that(question.quiz.name, equal_to(quiz_name))

    expected_first_question = question.quiz.first_question()
    actual_first_question = question.question
    assert_that(actual_first_question, equal_to(expected_first_question))


def save_quiz(context: Context, quiz: Quiz):
    controller: AuthorController = context.author_controller
    result = controller.save(quiz)
    assert_that(result.success, is_(True))


@when('the student answers "{answer}"')
def step_impl_student_gives_answer(context: Context, answer: str):
    question = current_question(context)
    controller = context.study_controller
    context.recent_answer = controller.record_answer_and_get_status(
        question_number=question.question_number,
        quiz=question.quiz,
        selection=answer,
        session_id=None)


@then("the answer is confirmed as correct")
def step_impl_answer_is_confirmed_correct(context: Context):
    assert_that(context.recent_answer.correct, "Answer should be correct")


@step("the confirmation message is delivered")
def step_impl_confirmation_message_is_delivered(context: Context):
    assert_that(context.recent_answer.confirmation, is_not(empty()))


@step('the next question is "{question_text}"')
def step_impl_next_question_text_given(context: Context, question_text: str):
    quiz: Quiz = context.recent_answer.quiz
    next_question_number: int = context.recent_answer.next_question_number
    question: Question = quiz.question_by_number(next_question_number)
    assert_that(question.text, equal_to(question_text))


@step("the log shows the question was answered {how}")
def step_impl_log_shows_question_answer(context: Context, how: str):
    study_controller: StudyController = context.study_controller
    session_id = context.recent_answer.session_id
    quiz_name = context.recent_answer.quiz.name
    question_number = context.recent_answer.question_number
    log: AnswerEntry = study_controller.get_log_message_for_question(
        session_id,
        quiz_name,
        question_number
    )
    user_choice = log.selection
    expected = (how == "correctly")
    assert_that(log.is_correct, equal_to(expected),
                f"User said '{user_choice}', which is answered {how}")


@when("the student provides these answers")
def step_impl_student_provides_multiple_answers(context: Context):
    controller = context.study_controller
    for row in context.table:
        answer, expected = row['answer'], row.get('expected', 'right')

        question = current_question(context)
        recent_answer: StudyController.RecordedAnswer = \
            controller.record_answer_and_get_status(
                question_number=question.question_number,
                quiz=question.quiz,
                selection=answer,
                session_id=None
            )
        if expected in 'wrong':
            assert_that(recent_answer.correct, is_(False))
        else:
            assert_that(recent_answer.correct, is_(True))
        context.recent_answer = recent_answer

        more_questions = recent_answer.next_question_number
        if more_questions:
            new_question = controller.prepare_quiz_question_document(
                recent_answer.quiz,
                recent_answer.next_question_number
            )
            context.current_question = new_question


@then("we have completed the quiz")
def step_impl_quiz_is_completed(context: Context):
    recent_answer: StudyController.RecordedAnswer = context.recent_answer
    assert_that(recent_answer.quiz_is_finished(), is_(True))


@step("no incorrect answers were given")
def step_impl_all_answers_correct(context: Context):
    session_id = context.recent_answer.session_id
    quiz_name = context.recent_answer.quiz.name

    study_controller: StudyController = context.study_controller
    wrong_answers = study_controller.number_of_incorrect_answers(session_id,
                                                                 quiz_name)
    assert_that(wrong_answers, equal_to(0))


@step("we cannot go to the next question")
def step_impl_no_next_question(context: Context):
    recent_answer: StudyController.RecordedAnswer = context.recent_answer
    assert_that(recent_answer.next_question_number, none())


@step("{oopses:d} incorrect answer was given")
def step_impl_answer_was_wrong(context: Context, oopses: int):
    recent_answer: StudyController.RecordedAnswer = context.recent_answer
    assert_that(oopses, equal_to(recent_answer.incorrect_answers))
