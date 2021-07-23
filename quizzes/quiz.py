""" doc string """
from dataclasses import dataclass, field

from quizzes.question import Question


@dataclass
class Quiz:
    """ questions to ask, with answers, and decoy answers"""
    name: str
    title: str
    questions: list[Question] = field(default_factory=list)

    @classmethod
    def from_json(cls, json_document):
        "Create a quiz from a json document"
        return Quiz(
            title=json_document.get('title', ''),
            name=json_document.get('name', ''),
            questions=[
                Question.from_json(q)
                for q in json_document.get('questions', [])
            ]
        )

    def has_questions(self):
        return len(self.questions) > 0

    def number_of_questions(self):
        return len(self.questions)

    def question_by_number(self, number: int) -> Question:
        return self.questions[number]

    def first_question(self):
        return (
            self.question_by_number(self.first_question_number())
            if self.has_questions()
            else None
        )

    def first_question_number(self):
        return 0 if self.has_questions() else None

    def last_question_number(self):
        if not self.has_questions():
            return None
        return max(0, self.number_of_questions() - 1)

    def next_question_number(self, number: int):
        """If there is a next question, returns the question number"""
        if not self.has_questions():
            return None
        likely_next = number + 1
        return (
            likely_next
            if likely_next <= self.last_question_number()
            else None
        )
