from behave import step, when, then
# use_step_matcher("re")
from behave.runner import Context
from hamcrest import assert_that, is_

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz


# pylint disable=no-member

@step("decoys are")
def step_impl_decoys_are(context: Context):
    only_row = context.table.row[0]
    context.decoys = [value.strip() for value in only_row.cells]

    # When the author adds a quiz with name "Test Quiz" and title "Test Title"


@when('the author adds a quiz with name "{name}" and title "{title}"')
def step_impl_add_quiz(context: Context, name: str, title: str):
    quiz = Quiz(name=name, title=title)
    controller: AuthorController = context.author_controller
    result = controller.save(quiz)
    assert_that(result.success, is_(True))


@then('"{quiz_name}" should be accessible')
def step_impl_quiz_accessible(context: Context, quiz_name: str):
    controller: AuthorController = context.author_controller
    assert_that(controller.quiz_exists(quiz_name), is_(True),
                f"Cannot access newly-created '{quiz_name}'")


@when('the author adds a question "{question_text}"')
def step_impl_adds_question(context: Context, question_text):
    raise NotImplementedError(
        'STEP: When the author adds a question "Is there a question here?"')


@step('the answer is "{answer}"')
def step_impl_answer_is_correct(context: Context, answer):
    raise NotImplementedError('STEP: * the answer is "Not Yet"')


@step('confirmation is "{confirmation}"')
def step_impl_confirmation_is(context: Context, confirmation):
    raise NotImplementedError(
        'STEP: * confirmation is "There is one to come which will be added"')


@then('there is one question in "{quiz_name}"')
def step_impl_there_is_one_question(context: Context, quiz_name):
    raise NotImplementedError('STEP: Then there is one question in "empty"')


@when("the author adds resources")
def step_impl_adds_resource(context: Context):
    raise NotImplementedError('WHEN: the author adds resources')


@then("the question has 2 resources")
def step_impl_question_has_resources(context: Context):
    raise NotImplementedError('STEP: Then the question has 2 resources')
