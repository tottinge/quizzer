from behave import *
from behave.runner import Context


@given('a student "{user_id}" exists with password "{password}"')
def step_impl(context: Context, user_id: str, password: str):
    # options:
    #   swap out the real user file, restore after
    #   redirect to read a different user file we create & write from here
    #   redirect to read a different user file we wrote in advance
    #   mock the reading of the user file (json.load)
    #   mock find_user_by_name

    raise NotImplementedError(
        u'STEP: Given a student "test_student" exists with password "testme"')
