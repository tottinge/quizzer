from behave import *


# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')


@given("a student starts quizzology")
def step_impl(context):
    pass


@step('we have a quiz called "{quizname}"')
def step_impl(context, quizname):
    raise NotImplementedError(
        u'STEP: And we have a quiz called "{quizname}"'.format(
            quizname=quizname))


@when('the student selects the quiz "cats"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the student selects the quiz "cats"')


@then('the "cats" quiz status is in-progress')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Then the "cats" quiz status is in-progress')


@step('the first "cats" question is displayed')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: And the first "cats" question is displayed')
