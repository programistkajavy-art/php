import json
from pathlib import Path

from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .game_logic import GAMES, GameError, create_game, game_response, submit_guess


BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    return FileResponse((BASE_DIR / "static" / "index.html").open("rb"))


def start_game(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    return JsonResponse(game_response(create_game()), status=201)


@csrf_exempt
def send_guess(request, game_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    game = GAMES.get(game_id)
    if game is None:
        return JsonResponse({"detail": "Gra nie istnieje"}, status=404)
    try:
        payload = json.loads(request.body or "{}")
        word = payload.get("word", "")
        submit_guess(game, word)
    except (json.JSONDecodeError, AttributeError, TypeError):
        return JsonResponse({"detail": "Nieprawidłowe dane JSON"}, status=400)
    except GameError as error:
        return JsonResponse({"detail": error.detail}, status=error.status_code)
    return JsonResponse(game_response(game))


def get_game(request, game_id):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    game = GAMES.get(game_id)
    if game is None:
        return JsonResponse({"detail": "Gra nie istnieje"}, status=404)
    return JsonResponse(game_response(game))
