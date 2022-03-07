from typing import Protocol, Optional, Union

from behave import given, when, then, step
from behave.runner import Context
from hamcrest import is_, assert_that, equal_to

from apps.author.author_controller import AuthorController
from quizzes.question import Question
from quizzes.quiz import Quiz


# use_step_matcher("cfparse")

class HasOurStuff(Protocol):
    author_controller: Optional[AuthorController]
    quiz: Optional[Quiz]


LocalContext = Union[HasOurStuff, Context]


@given('there is a quiz with name "{name}"')
def step_impl(context: LocalContext, name):
    quiz = Quiz(name=name, title=f"Title For Quiz Named {name}")
    result = context.author_controller.save(quiz)
    assert_that(result.success, is_(True))
    context.quiz = quiz


@when("a question is added")
def step_impl(context: LocalContext):
    table_values = dict(
        (row['FIELD'], row['VALUE'])
        for row in context.table.rows
    )
    text = table_values.get('question')
    answer = table_values.get('answer')
    confirmation = table_values.get('confirmation')
    question = Question(text, answer, confirmation=confirmation)
    quiz: Quiz = context.quiz
    quiz.add_question(question)
    controller: AuthorController = context.author_controller
    result = controller.save(quiz)
    assert_that(result.success, is_(True))


@then('there is {count} question in "{quiz_name}"')
def step_impl(context: LocalContext, count: str, quiz_name: str):
    api: AuthorController = context.author_controller
    quiz = api.get_quiz(quiz_name)
    assert_that(quiz.name, equal_to(quiz_name))
    assert_that(int(count), is_(quiz.number_of_questions()))


@step("has decoys")
def step_impl(context: LocalContext):
    question: Question = context.quiz.first_question()
    new_decoys = [row['DECOYS'] for row in context.table.rows]
    question.decoys = new_decoys
    context.author_controller.save(context.quiz)


@step("has resources")
def step_impl(context: LocalContext):
    question: Question = context.quiz.first_question()
    question.resources = [
        [row['DESCRIPTION'], row['URL']]
        for row in context.table.rows
    ]
    context.author_controller.save(context.quiz)


@step("the first question has")
def step_impl(context: LocalContext):
    first_row = context.table.rows[0]
    decoy_count = int(first_row['DECOYS'])
    resource_count = int(first_row['RESOURCES'])

    api: AuthorController = context.author_controller
    quiz: Quiz = api.get_quiz(context.quiz.name)

    first_question: Question = quiz.first_question()
    assert_that(len(first_question.decoys), is_(decoy_count))
    assert_that(len(first_question.resources), is_(resource_count))
