# Created by wpreid at 1/10/22

@wip
Feature: Authenticate User
  Explore the elements of authenticating users

  Scenario: Simple Student Login Success
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "testme"
    Then the session is directed to a non-login page

  Scenario: Simple Student Login Failure
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "wrong"
    Then the session is directed to the login page