from typing import NamedTuple, Iterable, Protocol, Optional

from quizzes.quiz import Quiz


class QuizSummary(NamedTuple):
    name: str
    title: str
    id: str
    image_url: Optional[str] = None


class SaveQuizResult(NamedTuple):
    id: str
    success: bool
    message: str


class StoresQuizzes(Protocol):
    def get_quiz_summaries(self) -> Iterable[QuizSummary]:
        ...

    def get_quiz(self, name: str) -> Optional[Quiz]:
        ...

    def save_quiz(self, quiz: Quiz) -> SaveQuizResult:
        ...

    def exists(self, quiz_name: str) -> bool:
        ...