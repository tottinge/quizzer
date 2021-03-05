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
        self.question = question
        self.decoys = decoys
        self.answer = answer
        self.resources = resources

    def is_correct_answer(self, selection: str):
        return self.answer == selection
