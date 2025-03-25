document.addEventListener('DOMContentLoaded', function() {
    let currentBet = 0;

    // Betting buttons
    document.querySelectorAll('.bet-btn').forEach(button => {
        button.addEventListener('click', () => {
            const amount = parseInt(button.dataset.amount);
            const playerChips = parseInt(document.getElementById('player-chips').textContent);

            if (playerChips >= amount) {
                currentBet += amount;
                document.getElementById('current-bet').textContent = currentBet;
                document.getElementById('player-chips').textContent = playerChips - amount;
                document.getElementById('deal-btn').disabled = false;
            }
        });
    });

    // Deal button
    document.getElementById('deal-btn').addEventListener('click', () => {
        fetch('/api/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ bet: currentBet })
        })
        .then(response => response.json())
        .then(updateGameState);
    });

    // Hit button
    document.getElementById('hit-btn').addEventListener('click', () => {
        fetch('/api/hit', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(updateGameState);
    });

    // Stand button
    document.getElementById('stand-btn').addEventListener('click', () => {
        fetch('/api/stand', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(updateGameState);
    });

    // Double Down button
    document.getElementById('double-btn').addEventListener('click', () => {
        fetch('/api/double_down', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(updateGameState);
    });

    function updateGameState(game) {
        // Update chips and bet
        document.getElementById('player-chips').textContent = game.player_chips;
        document.getElementById('current-bet').textContent = game.current_bet;

        // Update scores
        document.getElementById('player-score').textContent = game.player_score;
        document.getElementById('dealer-score').textContent =
            game.dealer_cards.some(card => card.is_face_down) ? '?' : game.dealer_score;

        // Update cards
        updateCards('player-cards', game.player_cards);
        updateCards('dealer-cards', game.dealer_cards);

        // Update controls visibility
        document.getElementById('betting-controls').style.display =
            game.game_active ? 'none' : 'flex';
        document.getElementById('game-controls').style.display =
            game.game_active ? 'flex' : 'none';

        // Enable/disable double down
        document.getElementById('double-btn').disabled =
            game.player_cards.length !== 2 || game.player_chips < game.current_bet;

        // Check for game end
        if (!game.game_active && game.current_bet === 0) {
            currentBet = 0;
            document.getElementById('deal-btn').disabled = true;
        }
    }

    function updateCards(containerId, cards) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';

        cards.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.className = `card ${card.suit === '♥' || card.suit === '♦' ? 'red' : ''}`;

            if (card.is_face_down) {
                cardElement.classList.add('face-down');
            } else {
                cardElement.textContent = `${card.value}${card.suit}`;
            }

            container.appendChild(cardElement);
        });
    }
});
