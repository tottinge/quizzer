from typing import NamedTuple, Iterable, Protocol

from quizzes.quiz import Quiz


class QuizSummary(NamedTuple):
    name: str
    title: str
    id: str
    image_url: str = None


class SaveQuizResult(NamedTuple):
    id: str
    success: bool
    message: str


class StoresQuizzes(Protocol):
    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        ...

    def get_quiz(self, name: str) -> Quiz:
        ...

    def save_quiz(self, quiz: Quiz) -> QuizSummary:
        ...

    def exists(self, quiz_name: str) -> bool:
        ...
