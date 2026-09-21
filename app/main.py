from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .game import GAMES, create_game, game_response, submit_guess
from .schemas import GameResponse, GuessRequest

app = FastAPI(title="Polskie Wordle")
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/games", response_model=GameResponse, status_code=201)
def start_game() -> dict:
    return game_response(create_game())


@app.post("/api/games/{game_id}/guesses", response_model=GameResponse)
def send_guess(game_id: str, request: GuessRequest) -> dict:
    game = GAMES.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Gra nie istnieje")
    submit_guess(game, request.word)
    return game_response(game)


@app.get("/api/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str) -> dict:
    game = GAMES.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Gra nie istnieje")
    return game_response(game)
