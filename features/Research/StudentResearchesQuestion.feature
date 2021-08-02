# Created by wpreid at 5/12/21
@JIRA_DEX-111
Feature: Student Researchs A Question
  As a Student,
  I want to use the resources provided on a question
  so that I can learn more

  http://www.google.com

  Background:
    Given quizzology is running


  @future
  Scenario: Student researches topic
  I have a lovely bunch of coconuts

    Given we have a quiz called "cats" with questions
      | question                       | answer |
      | How many feet on a normal cat? | 4      |
#    And associated research text
#      """ slklkslsakdflkjsdf
#        asdlkasdlkasldkj
#        laskdlkadsjkldf;as
#      """