# Created by wpreid at 7/29/21
@future
Feature: Edit Quiz
  # Enter feature description here

  Background:
    Given quizzology is running
    And there is a quiz with name "Test Quiz"

  Scenario: Add the first question to a quiz
    Given there is a quiz named "empty" with 0 questions

    And a question is created
      | question     | Are the tomatoes ripe?                       |
      | answer       | Not yet                                      |
      | confirmation | Tomatoes ripen in their own time. Be patient |
    * with decoys
      | always     |
      | never      |
    * with resources:
      | http://google.com         | Try google!                            |
      | http://stackoverflow.com/ | try someone else's answer              |
      | http://facebook.com/      | use conspiracy theories and falsehoods |

    When the author adds the question

    Then there is 1 question in "empty"
    And the first question has
      | Decoys | Resources |
      | 3      | 0         |

  Scenario: Author adds resources to a question
    Given there is a quiz named "populated" with 1 question
    When the author adds resources
      | Text                       | Url                                   |
      | Let me google that for you | http://lmgtfy.com/                    |
      | And then there was one     | http://wikipedia.com?Agatha%20Cristie |
    Then the question has 2 resources



  # Delete questions
  # Delete the quiz
  # change the title
  # change the name
  # Change question text
  # Change question answer
  # change question decoys
  # Change the confirmation message
  # add/delete/update question resources
  # check resource links
  # Duplicate a question within the quiz
  # Duplicate a question to a different quiz
  # Reorder quiz questions