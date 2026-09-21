from typing import Literal

from pydantic import BaseModel, Field


LetterStatus = Literal["correct", "present", "absent"]
GameStatus = Literal["active", "won", "lost"]


class GuessRequest(BaseModel):
    word: str = Field(min_length=5, max_length=5)


class GuessResponse(BaseModel):
    word: str
    statuses: list[LetterStatus]
    attempt_number: int


class GameResponse(BaseModel):
    game_id: str
    status: GameStatus
    attempts_used: int
    guesses: list[GuessResponse]
    target_word: str | None = None
