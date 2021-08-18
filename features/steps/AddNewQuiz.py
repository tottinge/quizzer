from typing import List

from behave import *
# use_step_matcher("re")
from behave.runner import Context
from hamcrest import assert_that, not_none, is_, has_item, is_in, equal_to

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from studycontroller import StudyController


@step("decoys are")
def step_impl(context: Context):
    only_row = context.table.row[0]
    context.decoys = [value.strip() for value in only_row.cells]

    # When the author adds a quiz with name "Test Quiz" and title "Test Title"


@when('the author adds a quiz with name "{name}" and title "{title}"')
def step_impl(context: Context, name: str, title: str):
    quiz = Quiz(name, title)
    context.quiz = quiz
    model: StudyController = context.quizzology
    result = model.quiz_store.save_quiz(quiz)
    assert_that(result.success, is_(True))


@then("it should be accessible")
def step_impl(context: Context):
    app: StudyController = context.quizzology
    defined_quiz_names: List[str] = [summary.name
                        for summary in app.quiz_store.get_quiz_summaries()]
    assert_that(context.quiz.name, is_in(defined_quiz_names))


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
