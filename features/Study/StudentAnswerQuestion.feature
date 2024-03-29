# Created by wpreid at 4/20/21

@PRD_1.2.3
Feature: Answer Questions
  # Enter feature description here

  Background:
    Given quizzology is running
    And we have a quiz called "cats" with questions
      | text                           | answer | confirmation                                                                 |
      | How many feet on a normal cat? | 4      | All cats are 4-legged (quadripedal) animals                                  |
      | Do cats eat meat?              | yes    | Cats are obligate carnivores, meaning that they need to eat meat to survive. |
      | Is this the 3rd question?      | yes    | We only wrote three                                                          |
    And the student selects the quiz called "cats"
    And the first "cats" question is displayed

  @finished
  Scenario: Student answers first question correctly in two question quiz
    When the student answers "4"
    Then the answer is confirmed as correct
    And the confirmation message is delivered
    And the log shows the question was answered correctly
    And the next question is "Do cats eat meat?"

  @finished
  Scenario: Student answers first question incorrectly
    When the student answers "3"
    Then the log shows the question was answered badly
    And we cannot go to the next question

  @finished
  Scenario: We complete a quiz perfectly
    When the student provides these answers
      | answer |
      | 4      |
      | yes    |
      | yes    |
    Then we have completed the quiz
    And no incorrect answers were given

  @finished
  Scenario: We complete a quiz with a wrong answer
    When the student provides these answers
      | answer   | expected  |
      | 4        | right     |
      | hairball | wrong     |
      | yes      | corrected |
      | yes      | right     |
    Then we have completed the quiz
    And 1 incorrect answer was given
