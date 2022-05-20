# Created by wpreid at 7/29/21
@wip
Feature: Edit Quiz
  # Enter feature description here

  Background:
    Given quizzology is running
    And there is a quiz with name "quiz2edit"

  Scenario: Add a simple question to an empty quiz
    When a question is added
      | FIELD        | VALUE                                        |
      | question     | Are the tomatoes ripe?                       |
      | answer       | Not yet                                      |
      | confirmation | Tomatoes ripen in their own time. Be patient |
    Then there is 1 question in "quiz2edit"

  Scenario: Add a complete question to a quiz
    When a question is added
      | FIELD        | VALUE                                        |
      | question     | Are the tomatoes ripe?                       |
      | answer       | Not yet                                      |
      | confirmation | Tomatoes ripen in their own time. Be patient |
    And has decoys
      | DECOYS |
      | always |
      | never  |
    And has resources
      | URL                       | DESCRIPTION                            |
      | http://google.com         | Try google!                            |
      | http://stackoverflow.com/ | try someone else's answer              |
      | http://facebook.com/      | use conspiracy theories and falsehoods |
    Then there is 1 question in "quiz2edit"
    And the first question has
      | DECOYS | RESOURCES |
      | 2      | 3         |

  # ToDo: Additional Tests
  # Delete questions
  # Delete the quiz
  # check resource links
  # Duplicate a question within the quiz
  # Duplicate a question to a different quiz
  # Reorder quiz questions