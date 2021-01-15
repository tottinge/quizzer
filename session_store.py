from tinydb import Query


class AnswerEntry:
    """
    Record an answer given to a question in a test session.
    Whole-value class allows for evolution of records without breaking existing code.
    """

    def __init__(self, session_id, quiz_name, question_number, selection, is_correct):
        self.session_id = session_id
        self.quiz_name = quiz_name
        self.question_number = question_number
        self.selection = selection
        self.is_correct = is_correct

    def __eq__(self, other):
        return (
                self.session_id == other.session_id
                and self.quiz_name == other.quiz_name
                and self.question_number == other.question_number
                and self.selection == other.selection
                and self.is_correct == other.is_correct
        )

    def as_dict(self):
        return dict(
            session_id=self.session_id,
            quiz_name=self.quiz_name,
            question_number=self.question_number,
            selection=self.selection,
            is_correct=self.is_correct
        )
    @classmethod
    def from_dict(cls, record):
        return AnswerEntry(
            session_id=record["session_id"],
            quiz_name=record["quiz_name"],
            question_number=record["question_number"],
            selection=record["selection"],
            is_correct=record["is_correct"]
        )

class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """

    def __init__(self, storage=None):
        self.recorded_answers = []
        self.storage = storage

    def record_answer(self, session_id, quiz_name, question_number, selection, is_correct):
        record = AnswerEntry(session_id, quiz_name, question_number, selection, is_correct)
        self.recorded_answers.append(record)
        self.storage.insert(record.as_dict())

    def perfect_answers(self, session_id, quiz_name):
        query = Query()
        records = self.storage.search(query.session_id == session_id)
        result = [AnswerEntry.from_dict(x) for x in records]
        old_result = [item for item in self.recorded_answers
            if item.session_id == session_id
            and item.quiz_name == quiz_name
            and item.is_correct]

        return old_result


    def incorrect_answers(self, session_id, quiz_name):
        return [item for item in self.recorded_answers
                if item.session_id == session_id
                and item.quiz_name == quiz_name
                and not item.is_correct]

    def number_of_correct_answers(self, session_id, quiz_name):
        return len(self.perfect_answers(session_id, quiz_name))

    def number_of_incorrect_answers(self, session_id, quiz_name):
        return len(self.incorrect_answers(session_id, quiz_name))

    @staticmethod
    def get_new_session_id():
        import uuid
        return str(uuid.uuid4())

    def questions_answered_incorrectly(self, target_session):
        """
        Get a list of questions which were answered incorrectly
        at least once during a session.
        """
        return {(answer.quiz_name, answer.question_number)
                for answer in self.recorded_answers
                if answer.session_id == target_session and not answer.is_correct
                }

    def questions_answered_correctly(self, target_session):
        """
        Get a list of questions which were never answered incorrectly
        in a given session.
        """
        return {(answer.quiz_name, answer.question_number)
                for answer in self.recorded_answers
                if answer.session_id == target_session and answer.is_correct
                }
