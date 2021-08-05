# Created by wpreid at 7/29/21
@future
Feature: Quiz Authoring
  # Enter feature description here

  Background:
    Given quizzology is running

  Scenario: Create an empty quiz
    Given the author adds a quiz with name "Test Quiz" and title "Test Title"

    Then it should be accessible



  # Import a JSON quiz with unique name
  # Import a JSON quiz with duplicate name
  # Duplicate a quiz

