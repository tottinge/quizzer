from behave import *


# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')


@given("a student starts quizzology")
def step_impl(context):
    # Create a Quizzology object
    pass


@step('we have a quiz called "{quizname}"')
def step_impl(context, quizname):
    # Create a quiz in the session store
    raise NotImplementedError(
        u'STEP: And we have a quiz called "{quizname}"'.format(
            quizname=quizname))


@when('the student selects the quiz "cats"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Ask for question 1 in Cats Quiz
    raise NotImplementedError(u'STEP: When the student selects the quiz "cats"')


@then('the "cats" quiz status is in-progress')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    raise NotImplementedError(
        u'STEP: Then the "cats" quiz status is in-progress')


@step('the first "cats" question is displayed')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # The question number is the first question in cats
    raise NotImplementedError(
        u'STEP: And the first "cats" question is displayed')
