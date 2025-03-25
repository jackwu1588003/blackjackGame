from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from game_logic import BlackjackGame
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    if 'game' not in session:
        session['game'] = BlackjackGame()
    return render_template('index.html', game=session['game'].to_dict())


@app.route('/api/start_game', methods=['POST'])
def start_game():
    game = session['game']
    bet_amount = int(request.json.get('bet', 0))

    if bet_amount <= 0 or bet_amount > game.player_chips:
        return jsonify({'error': 'Invalid bet amount'}), 400

    game.current_bet = bet_amount
    game.player_chips -= bet_amount
    game.game_active = True
    game.deal_initial_cards()

    session['game'] = game
    return jsonify(game.to_dict())


@app.route('/api/hit', methods=['POST'])
def hit():
    game = session['game']

    if not game.game_active:
        return jsonify({'error': 'Game not active'}), 400

    game.player_cards.append(game.draw_card())
    player_score = game.calculate_score(game.player_cards)

    if player_score > 21:
        game.game_active = False
        # Reveal dealer's cards
        for card in game.dealer_cards:
            card.is_face_down = False

    session['game'] = game
    return jsonify(game.to_dict())


@app.route('/api/stand', methods=['POST'])
def stand():
    game = session['game']

    if not game.game_active:
        return jsonify({'error': 'Game not active'}), 400

    # Reveal dealer's cards
    for card in game.dealer_cards:
        card.is_face_down = False

    # Dealer draws cards until score is 17 or higher
    while game.calculate_score(game.dealer_cards) < 17:
        game.dealer_cards.append(game.draw_card())

    dealer_score = game.calculate_score(game.dealer_cards)
    player_score = game.calculate_score(game.player_cards)

    # Determine winner and adjust chips
    if dealer_score > 21 or player_score > dealer_score:
        game.player_chips += game.current_bet * 2
    elif player_score == dealer_score:
        game.player_chips += game.current_bet

    game.game_active = False
    game.current_bet = 0

    session['game'] = game
    return jsonify(game.to_dict())


@app.route('/api/double_down', methods=['POST'])
def double_down():
    game = session['game']

    if not game.game_active or len(game.player_cards) != 2 or game.player_chips < game.current_bet:
        return jsonify({'error': 'Cannot double down'}), 400

    game.player_chips -= game.current_bet
    game.current_bet *= 2

    # Draw one card and stand
    game.player_cards.append(game.draw_card())

    return stand()


@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    session['game'] = BlackjackGame()
    return jsonify(session['game'].to_dict())


if __name__ == '__main__':
    app.run()
