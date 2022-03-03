Feature: Quiz Authoring
  The author should be able to create a quiz from scratch,
  duplicate an existing quiz, or load a quiz from a JSON
  file.
  If authoring is easy, it's more likely that the quiz app
  will be used, compared to the hassle of editing json files
  directly.

  Background:
    Given quizzology is running

  @finished
  Scenario: Create an empty quiz
    When the author adds a quiz with name "Test Quiz" and title "Test Title"
    Then "Test Quiz" should be accessible



  Scenario: Import a JSON quiz with unique name
  Scenario: Import a JSON quiz with duplicate name
  Scenario: Duplicate a quiz

