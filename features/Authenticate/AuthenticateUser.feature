# Created by wpreid at 1/10/22


Feature: Authenticate User
  Explore the elements of authenticating users

  Scenario: Simple Student Login Success
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "testme"
    Then "test_student" is authenticated
    And the assigned role is "student"

  Scenario: Simple Student Login Failure
    Given a student "test_student" exists with password "testme"
    When "test_student" logs in with password "wrong"
    Then "test_student" is not authenticated

  Scenario: Unknown person logs in and is assigned guest role
    Given user "fred" does not exist
    When "fred" logs in with password "wrong"
    Then "fred" is authenticated
    And the assigned role is "guest"

  Scenario: Simple Author Login Success
    Given an author "test_author" exists with password "testme"
    When "test_author" logs in with password "testme"
    Then "test_author" is authenticated
    And the assigned role is "author"

  Scenario: Simple Author Login Failure
    Given an author "test_author" exists with password "testme"
    When "test_author" logs in with password "wrongpass"
    Then "test_author" is not authenticated

  @WIP
  Scenario: Authenticated user session times out
    Given an author "test_author" exists with password "testme"
    And the session has expired
    When they visit a restricted page
    Then they should be challenged to re-login

