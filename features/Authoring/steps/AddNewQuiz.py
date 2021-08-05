from behave import *
# use_step_matcher("re")
from behave.runner import Context
from hamcrest import assert_that, not_none
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology
from sessions.session_store import SessionStore


# @given("quizzology is running")
# def step_impl(context: Context):
#     quizzology: Quizzology = Quizzology()
#     assert quizzology is not None
#     quizzology.set_quiz_store(QuizStore(context.temporary_directory.name))
#     session_store = SessionStore(TinyDB(storage=MemoryStorage))
#     quizzology.set_session_store(session_store)
#     context.quizzology = quizzology

@step("decoys are")
def step_impl(context: Context):
    only_row = context.table.row[0]
    context.decoys = [value.strip() for value in only_row.cells]

    # When the author adds a quiz with name "Test Quiz" and title "Test Title"

@given('the author adds a quiz with name "Test Quiz" and title "Test Title"')
@when('the author adds a quiz with name "{name}" and title "{title}"')
def step_impl(context: Context, name: str, title: str):
    assert_that(context.temporary_directory, not_none())
    quiz = Quiz(name, title)
    context.quiz = quiz
    raise NotImplementedError("No way to save a quiz yet")


@then("it should exist")
def step_impl(context: Context):
    raise NotImplementedError(u'STEP: Then it should exist')


@given('there is a quiz named "{name}" with {questions} questions')
@given('there is a quiz named "{name}" with {questions} question')
def step_impl(context: Context, name, questions):
    quiz = Quiz(name=name, title=name, questions=[])
    raise NotImplementedError("Quiz store can't create")


@when('the author adds a question "{question_text}"')
def step_impl(context: Context, question_text):
    raise NotImplementedError(
        u'STEP: When the author adds a question "Is there a question here?"')


@step('the answer is "{answer}"')
def step_impl(context: Context, answer):
    raise NotImplementedError(u'STEP: * the answer is "Not Yet"')


@step('confirmation is "{confirmation}"')
def step_impl(context: Context, confirmation):
    raise NotImplementedError(
        u'STEP: * confirmation is "There is one to come which will be added"')


@then('there is one question in "{quiz_name}"')
def step_impl(context: Context, quiz_name):
    raise NotImplementedError(u'STEP: Then there is one question in "empty"')


@step("the first question has")
def step_impl(context: Context):
    raise NotImplementedError(u'''STEP: And the first question has
                              | Decoys | Resources |
                              | 3 | 2 | ''')


@when("the author adds resources")
def step_impl(context: Context):
    raise NotImplementedError(u'''STEP: When the author adds resources
                              | Text | Url |
                              | Let
    me
    google
    that
    for you | http: //
        lmgtfy.com / |
        | And
    then
    there
    was
    one | http: // wikipedia.com?Agatha % 20
    Cristie | ''')


@then("the question has 2 resources")
def step_impl(context: Context):
    raise NotImplementedError(u'STEP: Then the question has 2 resources')


