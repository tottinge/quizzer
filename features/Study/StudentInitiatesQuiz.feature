# Created by wpreid at 5/12/21
Feature: Student Initiates Quiz
  As a Student, I want to initiate a quiz, so that I can test my knowledge

  Background:
    Given quizzology is running

  @finished
  Scenario: Student successfully initiates Cats Quiz
    Given we have a quiz called "cats" with questions
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
      | Do cats eat meat?              | yes    |
    When the student selects the quiz called "cats"
    Then the first "cats" question is displayed

