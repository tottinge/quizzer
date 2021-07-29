# Created by wpreid at 7/29/21
@future
Feature: Quiz Authoring
  # Enter feature description here

  @future
  Scenario: Create an empty quiz

    When I add a quiz with name "Test Quiz" and title "blah"
    Then it should exist
