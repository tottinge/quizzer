Feature: Basic Quiz Operations

  Scenario: Student initiates quiz
    Given a student starts quizzology
    And we have a quiz called "cats"
    When the student selects the quiz "cats"
    Then the "cats" quiz status is in-progress
    And the first "cats" question is displayed