# Polskie Wordle - backend

## Uruchomienie

Ta wersja przechowuje gry i próby wyłącznie w pamięci procesu. Po restarcie serwera są usuwane. Lista słów jest przechowywana w tabeli `game_word` w Azure SQL.

Zainstaluj zależności i uruchom:

```powershell
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_words
python manage.py runserver
```

Uzupełnij `.env` danymi połączenia do Azure SQL przed uruchomieniem migracji:

```env
AZURE_SQL_DATABASE=wordle
AZURE_SQL_HOST=twoj-serwer.database.windows.net
AZURE_SQL_USER=login_sql
AZURE_SQL_PASSWORD=haslo_sql
AZURE_SQL_PORT=1433
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
```

Plik `.env` nie powinien być dodawany do repozytorium. Na Windows musi być również zainstalowany Microsoft ODBC Driver 18 for SQL Server, a publiczny adres IP komputera musi być dopuszczony w regułach zapory Azure SQL.

API jest dostępne pod `http://127.0.0.1:8000`.

- `POST /api/games` rozpoczyna grę.
- `POST /api/games/{game_id}/guesses` przyjmuje próbę, np. `{ "word": "lampa" }`.
- `GET /api/games/{game_id}` pobiera stan gry.

Słowa można zmieniać w `data/words.txt`, a następnie ponownie uruchomić `python manage.py seed_words`. Gry i próby nadal nie są zapisywane w bazie.
