from tempfile import TemporaryDirectory
from typing import Protocol, Union, Optional, Dict, Callable
from unittest.mock import patch

import bs4
from behave import when, then, step, given
from behave.runner import Context
from hamcrest import assert_that, not_none, equal_to, is_, contains_string

import main
import security.authz
from main import authenticate, make_bearer_token
from shared.user import UserDatabase, User


class HasAUser(Protocol):
    authenticated_user: Optional[User]


class HasATempDir(Protocol):
    temporary_directory: Optional[TemporaryDirectory]


class HasAUserDb(Protocol):
    user_db: Optional[UserDatabase]


class HasRoutes(Protocol):
    routes: Optional[Dict[str, Callable[[], str]]]


class HasVisitResult(Protocol):
    visit_result: Optional[str]


OurContext = Union[
    HasAUser, HasATempDir, HasAUserDb, HasRoutes, HasVisitResult, Context
]


def get_user_db(context: OurContext):
    if not hasattr(context, "user_db"):
        context.user_db = UserDatabase(context.temporary_directory.name)
    return context.user_db


@step('"{user_id}" logs in with password "{password}"')
def step_impl(context: OurContext, user_id: str, password: str):
    context.authenticated_user = authenticate(user_id, password,
                                              db=get_user_db(context))
    if context.authenticated_user:
        token = make_bearer_token(user=context.authenticated_user)
        context.get_token_mock = patch("main.get_authorization_token",
                                       return_value=token)
        context.get_token_mock.start()


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
                                      hours_to_live=-1)
    context.get_token_mock = patch("main.get_authorization_token",
                                   return_value=expired_token)
    context.get_token_mock.start()


@given('an {role} "{user_id}" has logged in with password "{password}"')
def step_impl(context: OurContext, role: str, user_id: str, password: str):
    context.execute_steps(f"""
        Given a {role} "{user_id}" exists with password "{password}"
        And "{user_id}" logs in with password "{password}"
    """)


@given('the page "{pagename}" is restricted to {role}')
def step_impl(context: OurContext, pagename: str, role: str):
    roles = [r.strip() for r in role.split(",")]
    role_decorator = security.authz.require_roles(*roles)
    protected_function = role_decorator(lambda: pagename)
    set_route(context, pagename, protected_function)


def set_route(context, pagename, protected_function):
    routes = getattr(context, 'routes', {})
    routes[pagename] = protected_function
    context.routes = routes


@when('"{user}" visits "{route}"')
def step_impl(context: OurContext, user: str, route: str):
    mock = patch('main.get_request_path', return_value=route)
    mock.start()
    context.get_request_path_mock = mock
    context.visit_result = context.routes[route]()


@when('guest user visits "{route}"')
def step_impl(context: OurContext, route: str):
    role, user_name, password = None, 'nonesuch', 'nonesuch'
    context.execute_steps(f"""
        When "{user_name}" logs in with password "{password}"
        And "{user_name}" visits "{route}"
    """)


@then("they should be challenged to re-login")
def step_impl(context: OurContext):
    is_login_page(context)


def is_login_page(context):
    result = bs4.BeautifulSoup(context.visit_result, "html.parser")
    assert_that(result.head.title.text, contains_string('Who are you'))


@step("a flash message is displayed")
def step_impl(context: OurContext):
    result = bs4.BeautifulSoup(context.visit_result, "html.parser")
    flash = result.body.find("section", id='flash')
    assert_that(flash, not_none())


@then('the "{expected_page}" is visited')
def step_impl(context: OurContext, expected_page: str):
    if expected_page == "login":
        is_login_page(context)
    else:
        assert_that(context.visit_result, is_(expected_page))


@step('the destination "{page}" is passed to the login page')
def step_impl(context: OurContext, page: str):
    result = bs4.BeautifulSoup(context.visit_result, "html.parser")
    destination = result.body.find('input', attrs={"name":"destination"})
    assert_that(destination["value"], is_(page))