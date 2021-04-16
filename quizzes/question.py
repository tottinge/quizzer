from typing import NamedTuple


class Question(NamedTuple):
    question: str
    answer: str
    decoys: list[str] = []
    resources: list[list[str]] = []
    confirmation: str = ''

    @staticmethod
    def from_json(json_document):
        return Question(**json_document)

    def is_correct_answer(self, selection: str):
        return self.answer == selection
