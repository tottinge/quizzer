import hamcrest
from behave import *
from behave.runner import Context
from hamcrest import assert_that, not_none, equal_to

from main import create_user, authenticate


@given('a student "{user_id}" exists with password "{password}"')
def step_impl(context: Context, user_id: str, password: str):
    # options:
    #   swap out the real user file, restore after
    #   modify the actual user file, fix it after
    #   redirect to read a different user file we create & write from here
    #   redirect to read a different user file we wrote in advance
    #   mock the reading of the user file (json.load)
    #   mock find_user_by_name
    create_user(user_id, password=password, role='student',
                user_dir_name=context.temporary_directory.name)


@when('"{user_id}" logs in with password "{password}"')
def step_impl(context: Context, user_id: str, password:str):
    context.authenticated_user = authenticate(user_id, password)


@then('"{user_id}" is authenticated')
def step_impl(context: Context, user_id:str):
    user:dict = context.authenticated_user
    assert_that(user, not_none())
    assert_that(user['user_name'], equal_to(user_id))
