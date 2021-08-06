# Created by wpreid at 7/29/21
@future
Feature: Edit Quiz
  # Enter feature description here

  Background:
    Given quizzology is running
    And there is a quiz with name "Test Quiz"

  Scenario: Add the first question to a quiz
    Given there is a quiz named "empty" with 0 questions
    When the author adds a question "Is there a question here?"
    * the answer is "Not Yet"
    * decoys are
      | Yes | No | Unsure |
    * confirmation is "There is one to come which will be added"
    Then there is one question in "empty"
    And the first question has
      | Decoys | Resources |
      | 3      | 2         |

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