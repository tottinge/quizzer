from typing import NamedTuple, Iterable, Protocol, Optional

from .quiz import Quiz


class QuizSummary(NamedTuple):
    name: str
    title: str
    id: str
    image_url: str


class SaveQuizResult(NamedTuple):
    id: str
    success: bool
    message: str


class QuizStore(Protocol):
    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        ...

    def get_quiz(self, name: str) -> Optional[Quiz]:
        ...

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        ...

    def exists(self, quiz_name: str) -> bool:
        ...
