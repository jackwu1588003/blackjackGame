import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.is_face_down = False

    def to_dict(self):
        return {
            'suit': self.suit,
            'value': self.value,
            'is_face_down': self.is_face_down
        }

    def get_numeric_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        return int(self.value)


class BlackjackGame:
    def __init__(self):
        self.deck = []
        self.player_cards = []
        self.dealer_cards = []
        self.player_chips = 1000
        self.current_bet = 0
        self.insurance_bet = 0
        self.game_active = False
        self.create_new_deck()

    def create_new_deck(self, num_decks=6):
        self.deck = []
        for _ in range(num_decks):
            for suit in ['♠', '♥', '♦', '♣']:
                for value in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
                    self.deck.append(Card(suit, str(value)))
        random.shuffle(self.deck)

    def calculate_score(self, cards):
        score = 0
        aces = 0
        for card in cards:
            if not card.is_face_down:
                if card.value == 'A':
                    aces += 1
                else:
                    score += card.get_numeric_value()

        for _ in range(aces):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        return score

    def deal_initial_cards(self):
        self.player_cards = []
        self.dealer_cards = []

        # Deal cards alternately
        self.player_cards.append(self.draw_card())
        dealer_first = self.draw_card()
        self.dealer_cards.append(dealer_first)

        self.player_cards.append(self.draw_card())
        dealer_second = self.draw_card()
        dealer_second.is_face_down = True
        self.dealer_cards.append(dealer_second)

    def draw_card(self):
        if len(self.deck) < 20:  # Reshuffle when deck is low
            self.create_new_deck()
        return self.deck.pop()

    def to_dict(self):
        return {
            'player_cards': [card.to_dict() for card in self.player_cards],
            'dealer_cards': [card.to_dict() for card in self.dealer_cards],
            'player_chips': self.player_chips,
            'current_bet': self.current_bet,
            'insurance_bet': self.insurance_bet,
            'game_active': self.game_active,
            'player_score': self.calculate_score(self.player_cards),
            'dealer_score': self.calculate_score(self.dealer_cards)
        }
