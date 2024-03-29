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

# NULL CASES:
#  These are cases we discussed and decided they were not interesting
#  enough to implement:
#  Scenario: Logged-in user visits unrestricted page
#  Scenario: Unauthenticated user visits unrestricted page

  Scenario: Unauthenticated user visits student-restricted page
    Given the page "/student-only" is restricted to student
    When guest user visits "/student-only"
    Then they should be challenged to re-login
    And the destination "/student-only" is passed to the login page
    And a flash message is displayed


  Scenario Outline: Authenticated user visits restricted pages
    Given the page "<page>" is restricted to <allowed role>
    And an <user role> "<userid>" exists with password "<password>"
    And "<userid>" logs in with password "<password>"
    When "<userid>" visits "<page>"
    Then the "<expected page>" is visited

    Examples:
      | page                 | allowed role    | user role | userid       | password | expected page        |
      | student-only         | student         | student   | test_student | testme   | student-only         |
      | author-only          | author          | author    | test_author  | testme   | author-only          |
      | authors-and-students | author, student | student   | test_student | testme   | authors-and-students |
      | authors-and-students | author, student | editor    | test_student | testme   | login                |
      | student-only         | student         | author    | test_author  | testme   | login                |


  Scenario: Authenticated user session times out
    Given the page "/author-only" is restricted to author
    And an author "test_author" has logged in with password "testme"
    And the session has expired
    When "test_author" visits "/author-only"
    Then they should be challenged to re-login

