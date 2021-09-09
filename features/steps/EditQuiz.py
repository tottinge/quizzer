from behave import *
from behave.runner import Context
from hamcrest import is_, assert_that, equal_to

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


# ToDo - Should we be using the QuizStore or context to retrieve the quiz
#  Should we be reaching all the way into the QuizStore??
@then('there is {count} question in "{quiz_name}"')
def step_impl(context: Context, count: str, quiz_name: str):
    store: QuizStore = context.quizzology.quiz_store
    quiz: Quiz = store.get_quiz(quiz_name)
    assert_that(quiz.name, equal_to(quiz_name))
    assert_that(int(count), is_(quiz.number_of_questions()))

