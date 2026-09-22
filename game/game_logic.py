import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from django.db import OperationalError

from .models import Word

MAX_ATTEMPTS = 6
GAMES: dict[str, "Game"] = {}


class GameError(Exception):
	def __init__(self, detail: str, status_code: int):
		self.detail = detail
		self.status_code = status_code


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
	try:
		words = list(Word.objects.filter(is_active=True).values_list("word", flat=True))
	except OperationalError as error:
		raise GameError("Nie można odczytać słów z bazy danych", 503) from error
	if not words:
		raise GameError("Brak aktywnych słów w bazie danych", 503)

	game = Game(target_word=words[0])
	GAMES[game.id] = game
	return game


def submit_guess(game: Game, raw_word: str) -> Guess:
	word = normalize_word(raw_word)
	if len(word) != 5:
		raise GameError("Próba musi mieć dokładnie 5 liter", 422)
	if game.status != "active":
		raise GameError("Gra jest już zakończona", 409)
	if game.attempts_used >= MAX_ATTEMPTS:
		raise GameError("Wykorzystano wszystkie próby", 409)

	statuses = evaluate_guess(word, game.target_word)
	attempt_number = game.attempts_used + 1
	if word == game.target_word:
		game.status = "won"
	elif attempt_number == MAX_ATTEMPTS:
		game.status = "lost"

	guess = Guess(value=word, statuses=statuses, attempt_number=attempt_number)
	game.guesses.append(guess)
	return guess


def game_response(game: Game) -> dict:
	return {
		"game_id": game.id,
		"status": game.status,
		"attempts_used": game.attempts_used,
		"guesses": [
			{
				"word": guess.value,
				"statuses": guess.statuses,
				"attempt_number": guess.attempt_number,
			}
			for guess in game.guesses
		],
		"target_word": game.target_word if game.status != "active" else None,
	}
