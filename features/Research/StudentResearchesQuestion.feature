# Created by wpreid at 5/12/21
@PRD_1.2.55
Feature: Student Researchs A Question
  As a Student,
  I want to use the resources provided on a question
  so that I can learn more

  Background:
    Given a student starts quizzology


  @future
  Scenario: Student researches topic
    Given we have a quiz called "cats" with questions
      | question                       | answer | 
      | How many feet on a normal cat? | 4      |
