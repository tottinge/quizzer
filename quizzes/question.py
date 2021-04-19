from dataclasses import dataclass, field
from typing import NamedTuple

@dataclass
class Question():
    question: str
    answer: str
    decoys: list[str] = field(default_factory=list)
    resources: list[list[str]] = field(default_factory=list)
    confirmation: str = ''

    @staticmethod
    def from_json(json_document):
        return Question(**json_document)

    def is_correct_answer(self, selection: str):
        return self.answer == selection
