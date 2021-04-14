class Question:
    @staticmethod
    def from_json(json_document):
        return Question(
            question=json_document.get('question', ''),
            decoys=json_document.get('decoys', ''),
            answer=json_document.get('answer', ''),
            resources=json_document.get('resources', None),
            confirmation=json_document.get('confirmation','')
        )

    def __init__(self, question, decoys, answer, confirmation="", resources=None):
        self.confirmation = confirmation
        self.question = question
        self.decoys = decoys
        self.answer = answer
        self.resources = resources

    def is_correct_answer(self, selection: str):
        return self.answer == selection

    def to_dict(self):
        return dict(
            question = self.question,
            decoys = self.decoys,
            answer = self.answer,
            resources = self.resources,
            confirmation=self.confirmation
        )
