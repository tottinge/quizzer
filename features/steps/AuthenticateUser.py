from behave import *
from behave.runner import Context

from main import create_user


@given('a student "{user_id}" exists with password "{password}"')
def step_impl(context: Context, user_id: str, password: str):
    # options:
    #   swap out the real user file, restore after
    #   modify the actual user file, fix it after
    #   redirect to read a different user file we create & write from here
    #   redirect to read a different user file we wrote in advance
    #   mock the reading of the user file (json.load)
    #   mock find_user_by_name
    create_user(user_id, role='student', password=password,
                user_dir_name=context.temporary_directory.name)
