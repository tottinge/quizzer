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
  Scenario: Student answers first question correctly in two question quiz
    Given we have a quiz called "cats" with questions
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
      | Do cats eat meat?              | yes    |
    And the student selects the quiz called "cats"
#    And the first "cats" question is displayed
#    When the student answers "4"
#    Then the answer is confirmed as correct
#    And there is a link to the next question
#    And the log shows the first question was answered correctly

# ORIGINAL Scenario STEPS:
#    And the first question is presented
#    When the student answers "4"
#    Then the answer is confirmed as correct
#    And there is a link to the next question
#    And the log shows the first question was answered correctly


  @future
  Scenario: Student answers question incorrectly

  @future
  Scenario: Student researches topic

