import json
import os

from behave import *

# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from behave.runner import Context

from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology

quizzology: Quizzology = None
first_question = None


@given("a student starts quizzology")
def step_impl(context: Context):
    global quizzology
    quizzology = Quizzology()
    context.quizzology = quizzology
    assert quizzology is not None
    quizzology.set_quiz_store(QuizStore(context.temporary_directory.name))


@step('we have a quiz called "{quizname}"')
def step_impl(context: Context, quizname: str):
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
def step_impl(context: Context, quizname: str):
    # Ask for question 1 in Cats Quiz
    global first_question
    quiz = quizzology.get_quiz_by_name(quizname)
    first_question = quizzology.begin_quiz(quiz)


@then('the "{quizname}" quiz is in-progress')
def step_impl(context: Context, quizname: str):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    assert (
            first_question is not None
            and first_question["quiz"].name == quizname
    )


@step('the first "{quizname}" question is displayed')
def step_impl(context: Context, quizname: str):
    assert first_question is not None
    assert first_question["quiz"].name == quizname
    quiz = first_question["quiz"]
    expected_first_question = first_question["question"]
    actual_first_question = quiz.first_question()
    print(f"Expected {expected_first_question} got {actual_first_question}")
    assert actual_first_question == expected_first_question



@given('we have a quiz called "{quizname}" with questions')
def step_impl(context: Context, quizname: str):
    """
    :type context: behave.runner.Context
    """
    questions = [(row["question"], row["answer"]) for row in context.table]
    quiz = Quiz(title=quizname, name=quizname, questions=questions)
    save_quiz(context, quiz)


def save_quiz(context: Context, quiz: str):
    dir_name = context.temporary_directory.name
    filename = os.path.join(dir_name, quiz.name + ".json")
    with open(filename, "w") as output:
        json.dump(quiz.to_json(), output)

