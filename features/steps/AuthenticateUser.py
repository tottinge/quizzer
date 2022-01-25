from tempfile import TemporaryDirectory
from typing import Protocol, Union, Optional

from behave import *
from behave.runner import Context
from hamcrest import assert_that, not_none, equal_to, is_

from main import authenticate
from shared.user import UserDatabase, User


# Todo: should we consolidate our Protocols?
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


@given('a student "{user_id}" exists with password "{password}"')
def step_impl(context: OurContext, user_id: str, password: str):

    db = get_user_db(context)
    db.create_user(user_id, password=password, role='student')


@when('"{user_id}" logs in with password "{password}"')
def step_impl(context: OurContext, user_id: str, password: str):
    context.authenticated_user = authenticate(user_id, password,
                                              db=get_user_db(context))


@then('"{user_id}" is authenticated')
def step_impl(context: OurContext, user_id: str):
    user: User = context.authenticated_user
    assert_that(user, not_none())
    assert_that(user.user_name, equal_to(user_id))


@then('"{user_id}" is not authenticated')
def step_impl(context: Context, user_id: str):
    user: User = context.authenticated_user
    assert_that(user, is_(None))


@step('the assigned role is "{role}"')
def step_impl(context: Context, role: str):
    user: User = context.authenticated_user
    assert_that(user.role, is_(role))


@given('user "{user_id}" does not exist')
def step_impl(context: Context, user_id: str):
    db = get_user_db(context)
    found = db.find_user_by_name(user_name=user_id)
    assert_that(found, is_([]))
