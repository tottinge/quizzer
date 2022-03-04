from dataclasses import dataclass, field


@dataclass
class Question:
    question: str
    answer: str
    decoys: list[str] = field(default_factory=list)
    # ToDo: refactor resources to be a list of dict[str,str]
    resources: list[list[str]] = field(default_factory=list)
    confirmation: str = ''

    @staticmethod
    def from_json(json_document):
        return Question(**json_document)

    def is_correct_answer(self, selection: str):
        return self.answer == selection
