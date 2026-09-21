const board = document.querySelector('#board');
const form = document.querySelector('#guess-form');
const input = document.querySelector('#guess');
const message = document.querySelector('#message');
const newGameButton = document.querySelector('#new-game');

let gameId = null;
let gameFinished = false;

function showMessage(text, isError = false) {
  message.textContent = text;
  message.className = isError ? 'message error' : 'message';
}

function renderGame(game) {
  board.replaceChildren();
  for (let row = 0; row < 6; row += 1) {
    const guess = game.guesses[row];
    for (let column = 0; column < 5; column += 1) {
      const tile = document.createElement('div');
      tile.className = 'tile';
      if (guess) {
        tile.textContent = guess.word[column];
        tile.classList.add(guess.statuses[column]);
      }
      board.appendChild(tile);
    }
  }

  gameFinished = game.status !== 'active';
  input.disabled = gameFinished;
  form.querySelector('button').disabled = gameFinished;

  if (game.status === 'won') {
    showMessage(`Brawo! Słowo to ${game.target_word}.`);
  } else if (game.status === 'lost') {
    showMessage(`Koniec gry. Słowo to ${game.target_word}.`);
  }
}

async function startGame() {
  const response = await fetch('/api/games', { method: 'POST' });
  if (!response.ok) throw new Error('Nie udało się rozpocząć gry.');
  const game = await response.json();
  gameId = game.game_id;
  gameFinished = false;
  input.value = '';
  input.disabled = false;
  form.querySelector('button').disabled = false;
  showMessage('');
  renderGame(game);
  input.focus();
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const word = input.value.trim().toLowerCase();
  if (word.length !== 5 || gameFinished) return;

  const response = await fetch(`/api/games/${gameId}/guesses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ word }),
  });

  if (!response.ok) {
    const error = await response.json();
    showMessage(error.detail || 'Nie udało się wysłać próby.', true);
    return;
  }

  input.value = '';
  renderGame(await response.json());
  if (!gameFinished) input.focus();
});

newGameButton.addEventListener('click', () => startGame().catch((error) => showMessage(error.message, true)));
startGame().catch((error) => showMessage(error.message, true));
