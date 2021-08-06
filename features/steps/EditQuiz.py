from behave import *
from behave.runner import Context
from hamcrest import is_, assert_that

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
