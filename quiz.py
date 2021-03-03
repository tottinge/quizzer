""" doc string """
from box import Box


class Question(dict):
    pass


class Quiz(Box):
    """ questions to ask, with answers, and decoy answers"""

    def has_questions(self):
        return bool(self.questions)

    def number_of_questions(self):
        return len(self.questions)

    def question_by_number(self, number: int):
        return self.questions[number]

    def next_question_number(self, number: int):
        """If there is a next question, returns the question number"""
        if number + 1 >= len(self.questions):
            return None
        return number + 1
