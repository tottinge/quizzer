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
