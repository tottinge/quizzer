from behave import *


# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from quiz_store import QuizStore
from quizzology import Quizzology

quizzology = None
current_question_thingy = None

@given("a student starts quizzology")
def step_impl(context):
    global quizzology
    quizzology = Quizzology()
    quizzology.set_quiz_store( QuizStore() )


@step('we have a quiz called "{quizname}"')
def step_impl(context, quizname):
    raise NotImplementedError("We haven't figured this one out yet.")


@when('the student selects the quiz "cats"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Ask for question 1 in Cats Quiz
    global current_question_thingy
    quiz = quizzology.get_quiz_by_name('cats')
    current_question_thingy = Quizzology.prepare_quiz_question_document(quiz, 0)


@then('the "cats" quiz status is in-progress')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    assert (
        current_question_thingy is not None
        and current_question_thingy.quiz.name == "cats"
    )


@step('the first "cats" question is displayed')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # The question number is the first question in cats
    raise NotImplementedError(
        u'STEP: And the first "cats" question is displayed')
