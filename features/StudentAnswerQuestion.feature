# Created by wpreid at 4/20/21
Feature: Answer Questions
  # Enter feature description here

  Background:
    Given a student starts quizzology

  @finished
  Scenario: Student answers first question correctly in two question quiz
    Given we have a quiz called "cats" with questions
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
      | Do cats eat meat?              | yes    |
    And the student selects the quiz called "cats"
    And the first "cats" question is displayed
    When the student answers "4"
    Then the answer is confirmed as correct
    And the next question is "Do cats eat meat?"
    And the log shows the question was answered correctly


  @finished
  Scenario: Student's correct answer is confirmed
    Given we have a quiz called "cats" with questions
      | question                       | answer | confirmation                                                                 |
      | How many feet on a normal cat? | 4      | All cats are 4-legged (quadripedal) animals                                  |
      | Do cats eat meat?              | yes    | Cats are obligate carnivores, meaning that they need to eat meat to survive. |
    And the student selects the quiz called "cats"
    And the first "cats" question is displayed
    When the student answers "4"
    Then the log shows the question was answered correctly
    And the confirmation message is delivered


  @finished
  Scenario: Student answers first question incorrectly
    Given we have a quiz called "cats" with questions
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
      | Do cats eat meat?              | yes    |
    And the student selects the quiz called "cats"
    And the first "cats" question is displayed
    When the student answers "3"
    Then the log shows the question was answered badly

