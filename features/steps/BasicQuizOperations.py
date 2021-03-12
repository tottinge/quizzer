import json
import os

from behave import *

# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from quiz_store import QuizStore
from quizzology import Quizzology

quizzology: Quizzology = None
first_question = None


@given("a student starts quizzology")
def step_impl(context):
    global quizzology
    quizzology = Quizzology()
    assert quizzology is not None
    quizzology.set_quiz_store( QuizStore(context.temporary_directory.name) )


@step('we have a quiz called "{quizname}"')
def step_impl(context, quizname):
    filename = os.path.join(context.temporary_directory.name, quizname + ".json")
    with open(filename, "w") as json_file:
        document = {
            "name": quizname,
            "title": f"This is {quizname}"
        }
        json.dump(document, json_file)
    assert os.path.exists(filename)


@when('the student selects the quiz called "{quizname}"')
def step_impl(context, quizname: str):
    """
    :type context: behave.runner.Context
    """
    # Ask for question 1 in Cats Quiz
    global first_question
    print("Quiz store is using", quizzology.quiz_store.quiz_dir)
    quiz = quizzology.get_quiz_by_name(quizname)
    first_question = quizzology.begin_quiz(quiz)


@then('the "cats" quiz status is in-progress')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    assert (
            first_question is not None
            and first_question.quiz.name == "cats"
    )


@step('the first "cats" question is displayed')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # The question number is the first question in cats
    raise NotImplementedError(
        u'STEP: And the first "cats" question is displayed')
