import random
from collections import deque

class PlayingCard:
    CARD_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUIT_VALUES = ["♦️", "♣️", "♥️", "♠️"]

    def __init__(self, card_value, suit_value):
        self.card_value = card_value
        self.suit_value = suit_value

    def card_name(self):
        val_str = self.CARD_VALUES[self.card_value]
        suit_str = self.SUIT_VALUES[self.suit_value]
        card_str = f"{val_str} {suit_str}"
        if val_str == "10":
            return f"{card_str}"
        return f" {card_str}"

    def playing_card_value(self):
        return self.card_value

class PlayingCardDeck:
    def __init__(self):
        self.card_deck = []
        self.new_shuffle()

    """
    Create deck of cards by assigning a card value and a suit value.

    """
    def new_shuffle(self):
        cards = []

        for cv in range(len(PlayingCard.CARD_VALUES)):
            for sv in range(len(PlayingCard.SUIT_VALUES)):
                cards.append(PlayingCard(cv, sv))

        self.card_deck = []

        deck_size = len(PlayingCard.CARD_VALUES) * len(PlayingCard.SUIT_VALUES)

        for i in range(deck_size, 0, -1):
            rn = random.randint(0, i-1)
            self.card_deck.append(cards[rn])
            cards[rn] = cards[i-1]

    def next_card(self):
        if not self.is_empty():
            return self.card_deck.pop(0)
        return None

    def is_empty(self):
        return len(self.card_deck) == 0

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = deque()

    def add_card(self, card):
        self.cards.append(card)

    def play_card(self):
        if not self.is_empty():
            return self.cards.popleft()
        return None

    def add_cards(self, card_list):
        for card in card_list:
            self.cards.append(card)

    def card_count(self):
        return len(self.cards)

    def is_empty(self):
        return len(self.cards) == 0

class WarGame:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.rounds = 0
        self.deck = PlayingCardDeck()
        self.deal_cards()

    def deal_cards(self):
        for _ in range(26):
            self.player1.add_card(self.deck.next_card())
            self.player2.add_card(self.deck.next_card())
        print(f"Cards dealt: Player 1 has {self.player1.card_count()} cards, Player 2 has {self.player2.card_count()} cards.")


    def play_round(self):
        self.rounds += 1
        print(f"\nRound {self.rounds}:")

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()
        if card1 is None:
            return "Player 2"
        elif card2 is None:
            return "Player 1"

        print(f"{self.player1.name} plays {card1.card_name()}")
        print(f"{self.player2.name} plays {card2.card_name()}")

        pile = [card1, card2]
        result = self.compare_cards(card1, card2, pile)

        return result

    def compare_cards(self, card1, card2, pile):
        val1 = card1.playing_card_value()
        val2 = card2.playing_card_value()
        if val1 == val2:
            return self.handle_war(pile)

        if val1 > val2:
            print(f"{self.player1.name} wins the round!")
            self.player1.add_cards(pile)
        else:
            print(f"{self.player2.name} wins the round!")
            self.player2.add_cards(pile)

        print(f"Player 1 now has {self.player1.card_count()} cards, Player 2 has {self.player2.card_count()} cards.")
        return None

    def handle_war(self, pile):
        print("WAR!")

        if self.player1.card_count() < 4:
            print(f"{self.player1.name} doesn't have enough cards for war!")
            return "Player 2"
        elif self.player2.card_count() < 4:
            print(f"{self.player2.name} doesn't have enough cards for war!")
            return "Player 1"

        war_pile = pile.copy()

        print(f"{self.player1.name} puts down 3 cards face down")
        for _ in range(3):
            war_pile.append(self.player1.play_card())

        print(f"{self.player2.name} puts down 3 cards face down")
        for _ in range(3):
            war_pile.append(self.player2.play_card())

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        if card1 is None and card2 is None:
            print("Both players ran out of cards during war. It's a tie!")
            return "Tie"
        if card1 is None:
            print(f"{self.player1.name} ran out of cards during war!")
            return "Player 2"
        if card2 is None:
            print(f"{self.player2.name} ran out of cards during war!")
            return "Player 1"

        print(f"{self.player1.name} plays {card1.card_name()} for war")
        print(f"{self.player2.name} plays {card2.card_name()} for war")

        war_pile.extend([card1, card2])

        return self.compare_cards(card1, card2, war_pile)

    def play_game(self):
        print("Starting game of War!")
        winner = None

        while winner is None:
            winner = self.play_round()

            if self.rounds >= 10000:
                print("Game terminated after 10,000 rounds to prevent infinite loop.")
                if self.player1.card_count() > self.player2.card_count():
                    winner = "Player 1"
                elif self.player2.card_count() > self.player1.card_count():
                    winner = "Player 2"
                else:
                    winner = "Tie"

        print(f"\nGame over after {self.rounds} rounds!")
        if winner == "Tie":
            print("The game ended in a tie!")
        else:
            print(f"{winner} is the winner!")

if __name__ == "__main__":
    game = WarGame()
    game.play_game()
