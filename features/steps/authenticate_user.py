from tempfile import TemporaryDirectory
from typing import Protocol, Union, Optional, Dict, Callable
from unittest.mock import patch
from urllib.parse import urlparse, parse_qs

from behave import when, then, step, given
from behave.runner import Context
from bottle import HTTPResponse
from hamcrest import assert_that, not_none, equal_to, is_, contains_string

import security.authz
from security.authn import make_bearer_token, authenticate
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
def step_impl_user_logs_in(context: OurContext, user_id: str, password: str):
    context.authenticated_user = authenticate(user_id, password,
                                              db=get_user_db(context))
    if context.authenticated_user:
        token = make_bearer_token(user=context.authenticated_user)
        context.get_token_mock = patch("security.authz.get_authorization_token",
                                       return_value=token)
        context.get_token_mock.start()


@then('"{user_id}" is authenticated')
def step_impluser_is_authenticated(context: OurContext, user_id: str):
    user: User = context.authenticated_user
    assert_that(user, not_none())
    assert_that(user.user_name, equal_to(user_id))


@then('"{user_id}" is not authenticated')
def step_impl_user_is_not_authenticated(context: OurContext, user_id: str):
    user: Optional[User] = context.authenticated_user
    assert_that(user, is_(None))


@step('the assigned role is "{role}"')
def step_impl_assigned_role_is(context: OurContext, role: str):
    user: User = context.authenticated_user
    assert_that(user.role, is_(role))


@given('user "{user_id}" does not exist')
def step_impl_user_does_not_exist(context: OurContext, user_id: str):
    database = get_user_db(context)
    found = database.find_user_by_name(user_name=user_id)
    assert_that(found, is_([]))


@given('a {role} "{user_id}" exists with password "{password}"')
@given('an {role} "{user_id}" exists with password "{password}"')
def step_impl_user_exists_with_password(
        context: OurContext, role: str, user_id: str, password: str
    ):
    database = get_user_db(context)
    database.create_user(user_id, password=password, role=role)


@step("the session has expired")
def step_impl_session_has_expired(context: OurContext):
    expired_token = make_bearer_token(user=context.authenticated_user,
                                      hours_to_live=-1)
    context.get_token_mock = patch("security.authz.get_authorization_token",
                                   return_value=expired_token)
    context.get_token_mock.start()


@given('an {role} "{user_id}" has logged in with password "{password}"')
def step_impl_role_based_user_has_logged_in_with_password(
        context: OurContext, role: str, user_id: str, password: str
    ):
    context.execute_steps(f"""
        Given a {role} "{user_id}" exists with password "{password}"
        And "{user_id}" logs in with password "{password}"
    """)


@given('the page "{pagename}" is restricted to {role}')
def step_impl_page_is_restricted_to_role(
        context: OurContext, pagename: str, role: str
    ):
    roles = [r.strip() for r in role.split(",")]
    role_decorator = security.authz.require_roles(*roles)
    protected_function = role_decorator(lambda: pagename)
    set_route(context, pagename, protected_function)


def set_route(context, pagename, protected_function):
    routes = getattr(context, 'routes', {})
    routes[pagename] = protected_function
    context.routes = routes


@when('"{user}" visits "{route}"')
def step_impl_user_visits_route(context: OurContext, user: str, route: str):
    mock = patch('security.authz.get_request_path', return_value=route)
    mock.start()
    context.get_request_path_mock = mock
    guarded_route = context.routes[route]
    try:
        context.visit_result = guarded_route()
    except HTTPResponse as redirect:
        context.visit_result = redirect.get_header("Location")
        context.redirect_status = redirect.status


@when('guest user visits "{route}"')
def step_impl_guest_user_risits_route(context: OurContext, route: str):
    role, user_name, password = None, 'nonesuch', 'nonesuch'
    context.execute_steps(f"""
        When "{user_name}" logs in with password "{password}"
        And "{user_name}" visits "{route}"
    """)


@then("they should be challenged to re-login")
def step_impl_user_challenged_to_relogin(context: OurContext):
    is_login_page(context)


def is_login_page(context):
    assert_that(context.visit_result, contains_string('/login'))


@step("a flash message is displayed")
def step_impl_flash_message_displayed(context: OurContext):
    is_login_page(context)
    url_parse_result = urlparse(context.visit_result)
    query_parameters = parse_qs(url_parse_result.query)
    [flash] = query_parameters['flash']
    assert_that(flash, not_none())


@then('the "{expected_page}" is visited')
def step_impl_expected_page_is_visited(context: OurContext, expected_page: str):
    if expected_page == "login":
        is_login_page(context)
    else:
        assert_that(context.visit_result, is_(expected_page))


@step('the destination "{page}" is passed to the login page')
def step_impl_destination_page_is_passed_to_login_page(
        context: OurContext, page: str
    ):
    is_login_page(context)
    url_parse_result = urlparse(context.visit_result)
    query_parameters = parse_qs(url_parse_result.query)
    [destination] = query_parameters['destination']
    assert_that(destination, is_(page))
