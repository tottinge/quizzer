import uuid
from dataclasses import dataclass, field
from typing import Dict

def question_id_factory():
    return str(uuid.uuid4())

@dataclass
class Question:
    text: str
    answer: str
    decoys: list[str] = field(default_factory=list)
    resources: list[Dict[str, str]] = field(default_factory=list)
    confirmation: str = ''
    question_id: str = field(default_factory=question_id_factory)

    @staticmethod
    def from_json(json_document):
        return Question(**json_document)

    def is_correct_answer(self, selection: str):
        return self.answer == selection
