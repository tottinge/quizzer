from tempfile import TemporaryDirectory
from typing import Protocol, Union, Optional
from unittest.mock import patch

from behave import when, then, step, given
from behave.model import Step
from behave.runner import Context
from hamcrest import assert_that, not_none, equal_to, is_

import main
from main import authenticate, make_bearer_token
from shared.user import UserDatabase, User


class HasAUser(Protocol):
    authenticated_user: Optional[User]


class HasATempDir(Protocol):
    temporary_directory: Optional[TemporaryDirectory]


class HasAUserDb(Protocol):
    user_db: Optional[UserDatabase]


OurContext = Union[HasAUser, HasATempDir, HasAUserDb, Context]


def get_user_db(context: OurContext):
    if not hasattr(context, "user_db"):
        context.user_db = UserDatabase(context.temporary_directory.name)
    return context.user_db


@step('"{user_id}" logs in with password "{password}"')
def step_impl(context: OurContext, user_id: str, password: str):
    context.authenticated_user = authenticate(user_id, password,
                                              db=get_user_db(context))


@then('"{user_id}" is authenticated')
def step_impl(context: OurContext, user_id: str):
    user: User = context.authenticated_user
    assert_that(user, not_none())
    assert_that(user.user_name, equal_to(user_id))


@then('"{user_id}" is not authenticated')
def step_impl(context: OurContext, user_id: str):
    user: Optional[User] = context.authenticated_user
    assert_that(user, is_(None))


@step('the assigned role is "{role}"')
def step_impl(context: OurContext, role: str):
    user: User = context.authenticated_user
    assert_that(user.role, is_(role))


@given('user "{user_id}" does not exist')
def step_impl(context: OurContext, user_id: str):
    database = get_user_db(context)
    found = database.find_user_by_name(user_name=user_id)
    assert_that(found, is_([]))


@given('a {role} "{user_id}" exists with password "{password}"')
@given('an {role} "{user_id}" exists with password "{password}"')
def step_impl(context: OurContext, role: str, user_id: str, password: str):
    database = get_user_db(context)
    database.create_user(user_id, password=password, role=role)


@step("the session has expired")
def step_impl(context: OurContext):
    expired_token = make_bearer_token(user=context.authenticated_user,
                                      hours_to_live=0)
    context.get_token_mock = patch("main.get_authorization_token",
                                   return_value=expired_token)


@given('an {role} "{user_id}" has logged in with password "{password}"')
def step_impl(context: OurContext, role: str, user_id: str, password: str ):
    context.execute_steps(f"""
        Given a {role} "{user_id}" exists with password "{password}"
        And "{user_id}" logs in with password "{password}"
    """)
