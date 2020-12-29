""" doc string """
from box import Box


class Quiz(Box):
    """ Represents a collection of questions to ask, answers, and decoy answers"""
    def next_question_number(self, number):
        "If there is a next question, returns the question number"
        if number+1 >= len(self.questions):
            return None
        return number+1
