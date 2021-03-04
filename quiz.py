""" doc string """
from box import Box


class Question(Box):
    pass


class Quiz:
    """ questions to ask, with answers, and decoy answers"""

    def __init__(self, **kwargs):
        self.title=kwargs.get('title', '')
        self.name = kwargs.get('name','')
        self.questions = kwargs.get('questions', None)

    def has_questions(self):
        return bool(self.questions)

    def number_of_questions(self):
        return len(self.questions)

    def question_by_number(self, number: int):
        return Question(self.questions[number])

    def next_question_number(self, number: int):
        """If there is a next question, returns the question number"""
        if number + 1 >= len(self.questions):
            return None
        return number + 1
