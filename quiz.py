""" doc string """
from question import Question


class Quiz:
    """ questions to ask, with answers, and decoy answers"""

    @classmethod
    def from_json(cls, json_document):
        return Quiz(
            title=json_document.get('title', ''),
            name=json_document.get('name', ''),
            questions=[
                Question.from_json(q)
                for q in json_document.get('questions', [])
            ]
        )

    def __init__(self, title='', name='', questions=None):
        self.title = title
        self.name = name
        self.questions = questions if questions else []

    def has_questions(self):
        return len(self.questions) > 0

    def number_of_questions(self):
        return len(self.questions)

    def question_by_number(self, number: int) -> Question:
        return self.questions[number]

    def next_question_number(self, number: int):
        """If there is a next question, returns the question number"""
        if number + 1 >= len(self.questions):
            return None
        return number + 1
