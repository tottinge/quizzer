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
    quizzology.set_quiz_store(QuizStore(context.temporary_directory.name))


@step('we have a quiz called "{quizname}"')
def step_impl(context, quizname):
    filename = os.path.join(context.temporary_directory.name,
                            quizname + ".json")
    with open(filename, "w") as json_file:
        document = {
            "name": quizname,
            "title": f"This is {quizname}",
            "questions":[
                dict(question=f"{quizname}'s first", answer="?", decoys=[])
            ]
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


@then('the "{quizname}" quiz is in-progress')
def step_impl(context, quizname):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    assert (
            first_question is not None
            and first_question["quiz"].name == quizname
    )


@step('the first "{quizname}" question is displayed')
def step_impl(context, quizname):
    assert first_question is not None
    assert first_question["quiz"].name == quizname
    quiz = first_question["quiz"]
    expected_first_question = first_question["question"]
    actual_first_question = quiz.first_question()
    print(f"Expected {expected_first_question} got {actual_first_question}")
    assert actual_first_question == expected_first_question
