""" doc string """


class Question:
    @staticmethod
    def from_json(json_document):
        return Question(
            question=json_document.get('question', ''),
            answer=json_document.get('answer', ''),
            decoys=json_document.get('decoys', ''),
            resources=json_document.get('resources', None)
        )

    def __init__(self, question, decoys, answer, resources=None):
        self.resources = resources
        self.answer = answer
        self.decoys = decoys
        self.question = question

    def is_correct_answer(self, selection: str):
        return self.answer == selection


class Quiz:
    """ questions to ask, with answers, and decoy answers"""
    @classmethod
    def from_json(cls, json_document):
        return Quiz(
            title=json_document.get('title', ''),
            name=json_document.get('name', ''),
            questions = [
                Question.from_json(q)
                for q in json_document.get('questions', [])
            ]
        )

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.name = kwargs.get('name', '')
        self.questions = kwargs.get('questions',[])

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
