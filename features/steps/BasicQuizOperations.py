import json
import os

from behave import *

# use_step_matcher("re")
# @step('we have a quiz called "(.*)"')
from behave.runner import Context

from quizzes.question import Question
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from quizzology import Quizzology


@given("a student starts quizzology")
def step_impl(context: Context):
    quizzology = context.quizzology = Quizzology()
    assert quizzology is not None
    quizzology.set_quiz_store(QuizStore(context.temporary_directory.name))


@step('we have a quiz called "{quizname}"')
def step_impl(context: Context, quizname: str):
    questions = [Question(question=f"{quizname}'s first", answer="?", decoys=[])]
    quiz = Quiz(title=f"This is {quizname}", name=quizname, questions=questions)
    save_quiz(context, quiz)


@given('we have a quiz called "{quizname}" with questions')
def step_impl(context: Context, quizname: str):
    """
    :type context: behave.runner.Context
    """
    questions = [Question(question = row["question"],
                          answer = row["answer"],
                          decoys = [])
                 for row in context.table]
    quiz = Quiz(title=quizname, name=quizname, questions=questions)
    save_quiz(context, quiz)


@step('the student selects the quiz called "{quizname}"')
def step_impl(context: Context, quizname: str):
    quizzology = context.quizzology
    quiz = quizzology.get_quiz_by_name(quizname)
    context.current_question = quizzology.begin_quiz(quiz)


@then('the "{quizname}" quiz is in-progress')
def step_impl(context: Context, quizname: str):
    """
    :type context: behave.runner.Context
    """
    # Dictionary for selecting cats quiz contains cats quiz
    first_question = context.current_question
    assert (
            first_question is not None
            and first_question["quiz"].name == quizname
    )


@step('the first "{quizname}" question is displayed')
def step_impl(context: Context, quizname: str):
    first_question = context.current_question
    assert first_question is not None
    assert first_question["quiz"].name == quizname
    quiz = first_question["quiz"]
    expected_first_question = first_question["question"]
    actual_first_question = quiz.first_question()
    print(f"Expected {expected_first_question} got {actual_first_question}")
    assert actual_first_question == expected_first_question


def save_quiz(context: Context, quiz: Quiz):
    """
    This is done in the test helpers because authoring is not a feature
    of quizzology so far. When there is a proper authoring system, we will
    want to use its features rather than a test helper, so that we stop
    being data-structure-aware here.
    """
    dir_name = context.temporary_directory.name
    filename = os.path.join(dir_name, quiz.name + ".json")
    with open(filename, "w") as output:
        json.dump(quiz.to_dict(), output)


