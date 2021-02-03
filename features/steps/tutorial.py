from behave import *

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False

@given(u'a student starts quizzology')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a student starts quizzology')


@given(u'we have a quiz called "cats"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have a quiz called "cats"')


@when(u'the student selects the quiz "cats"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the student selects the quiz "cats"')


@then(u'the "cats" quiz status is in-progress')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the "cats" quiz status is in-progress')


@then(u'the first "cats" question is displayed')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the first "cats" question is displayed')
