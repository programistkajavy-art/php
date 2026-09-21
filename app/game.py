import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

MAX_ATTEMPTS = 6
SAMPLE_WORDS = ["domek", "lampa", "morze", "rzeka", "sanki", "szafa", "trawa"]
GAMES: dict[str, "Game"] = {}


@dataclass
class Guess:
    value: str
    statuses: list[str]
    attempt_number: int
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Game:
    target_word: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "active"
    guesses: list[Guess] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def attempts_used(self) -> int:
        return len(self.guesses)


def normalize_word(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip().lower())


def evaluate_guess(guess: str, target: str) -> list[str]:
    guess = normalize_word(guess)
    target = normalize_word(target)
    statuses = ["absent"] * len(guess)
    remaining = Counter()

    for index, letter in enumerate(guess):
        if letter == target[index]:
            statuses[index] = "correct"
        else:
            remaining[target[index]] += 1

    for index, letter in enumerate(guess):
        if statuses[index] == "correct":
            continue
        if remaining[letter] > 0:
            statuses[index] = "present"
            remaining[letter] -= 1

    return statuses


def create_game() -> Game:
    game = Game(target_word=SAMPLE_WORDS[0])
    GAMES[game.id] = game
    return game


def submit_guess(game: Game, raw_word: str) -> Guess:
    word = normalize_word(raw_word)
    if len(word) != 5:
        raise HTTPException(status_code=422, detail="Próba musi mieć dokładnie 5 liter")
    if game.status != "active":
        raise HTTPException(status_code=409, detail="Gra jest już zakończona")
    if game.attempts_used >= MAX_ATTEMPTS:
        raise HTTPException(status_code=409, detail="Wykorzystano wszystkie próby")

    statuses = evaluate_guess(word, game.target_word)
    attempt_number = game.attempts_used + 1
    if word == game.target_word:
        game.status = "won"
    elif attempt_number == MAX_ATTEMPTS:
        game.status = "lost"

    guess = Guess(value=word, statuses=statuses, attempt_number=attempt_number)
    game.guesses.append(guess)
    return guess


def guess_response(guess: Guess) -> dict:
    return {
        "word": guess.value,
        "statuses": guess.statuses,
        "attempt_number": guess.attempt_number,
    }


def game_response(game: Game) -> dict:
    response = {
        "game_id": game.id,
        "status": game.status,
        "attempts_used": game.attempts_used,
        "guesses": [guess_response(guess) for guess in game.guesses],
        "target_word": game.target_word if game.status != "active" else None,
    }
    return response
