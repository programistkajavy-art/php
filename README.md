# Polskie Wordle - backend

## Uruchomienie

Ta prosta wersja przechowuje gry wyłącznie w pamięci procesu. Po restarcie serwera gry są usuwane.

Zainstaluj zależności i uruchom:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API jest dostępne pod `http://127.0.0.1:8000`.

- `POST /api/games` rozpoczyna grę.
- `POST /api/games/{game_id}/guesses` przyjmuje próbę, np. `{ "word": "lampa" }`.
- `GET /api/games/{game_id}` pobiera stan gry.

Backend korzysta z małej listy przykładowych polskich słów. PostgreSQL, zapis historii i ranking zostaną dodane w kolejnym etapie.
