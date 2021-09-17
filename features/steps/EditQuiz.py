from behave import *
from behave.runner import Context
from hamcrest import is_, assert_that, equal_to

from apps.author.author_controller import AuthorController
from quizzes.question import Question
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore


# use_step_matcher("cfparse")


@given('there is a quiz with name "{name}"')
def step_impl(context: Context, name):
    quiz = Quiz(name=name, title=f"Title For Quiz Named {name}")
    store: QuizStore = context.quizzology.quiz_store
    result = store.save_quiz(quiz)
    assert_that(result.success, is_(True))
    context.quiz = quiz


@when("a question is added")
def step_impl(context: Context):
    table_values = dict(
        (row['Field'], row['Value'])
        for row in context.table.rows
    )
    text = table_values.get('question')
    answer = table_values.get('answer')
    confirmation = table_values.get('confirmation')
    question = Question(text, answer, confirmation=confirmation)
    quiz: Quiz = context.quiz
    quiz.add_question(question)
    store: QuizStore = context.quizzology.quiz_store
    store.save_quiz(quiz)


@then('there is {count} question in "{quiz_name}"')
def step_impl(context: Context, count: str, quiz_name: str):
    api: AuthorController = context.author_controller
    quiz = api.get_quiz(quiz_name)
    assert_that(quiz.name, equal_to(quiz_name))
    assert_that(int(count), is_(quiz.number_of_questions()))

