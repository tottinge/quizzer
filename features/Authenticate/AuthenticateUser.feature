# Created by wpreid at 1/10/22
Feature: Authenticate User
  Explore the elements of authenticating users

  Scenario: Simple Login Success
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "testme"
    Then the session is directed to a non-login page

  Scenario: Simple Login Failure
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "wrong"
    Then the session is directed to the login page