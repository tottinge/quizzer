Feature: Basic Quiz Operations

  Background:
    Given a student starts quizzology

  @finished
  Scenario: Student initiates quiz
    Given we have a quiz called "cats"
    When the student selects the quiz called "cats"
    Then the "cats" quiz is in-progress
    And the first "cats" question is displayed

  @wip
  Scenario: Student answers question correctly
    Given we have a quiz called "cats"
    And we have questions:
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
    And the student selects the quiz called "cats"
    When the student answers "4"
    Then the message "Your answer "4" is correct" is delivered



  @wip
  Scenario: Student answers question incorrectly

  @wip
  Scenario: Student researches topic

