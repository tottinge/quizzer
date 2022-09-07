import logging
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Protocol

logger = logging.getLogger(__name__)


@dataclass
class AnswerEntry:
    session_id: str
    quiz_name: str
    question_number: int
    selection: str
    is_correct: bool
    question_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat)

    @classmethod
    def from_dict(cls, dictionary):
        return AnswerEntry(**dictionary)


class SessionStore(Protocol):
    @abstractmethod
    def record_answer(self, session_id, quiz_name, question_number, selection,
                      is_correct, question_id, timestamp=None):
        ...

    @abstractmethod
    def perfect_answers(self, session_id, quiz_name) -> List[AnswerEntry]:
        ...

    @abstractmethod
    def number_of_incorrect_answers(self, session_id, quiz_name) -> int:
        ...

    @abstractmethod
    def get_all(self):
        ...

    @abstractmethod
    def get_log_message(self, session_id, quiz_name, question_number) \
            -> AnswerEntry:
        ...


