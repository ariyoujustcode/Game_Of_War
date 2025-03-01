import random
from collections import deque

# Card in a deck
class PlayingCard:
    # card values and suits
    CARD_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUIT_VALUES = ["D", "C", "H", "S"]

    # constructor
    def __init__(self, card_value, suit_value):
        self.card_value = card_value
        self.suit_value = suit_value

    # get the card information
    def card_name(self):
        return f"{self.CARD_VALUES[self.card_value]} {self.SUIT_VALUES[self.suit_value]}"

    # get only the card value
    def playing_card_value(self):
        return self.card_value

# Deck of cards
class PlayingCardDeck:
    # constructor
    def __init__(self):
        self.card_deck = []
        self.new_shuffle()

    """
    Create deck of cards by assigning a card value and a suit value.

    """
    def new_shuffle(self):
        # Empty array to hold cards
        cards = []

        # Add playing cards to deck by value and suit
        for cv in range(len(PlayingCard.CARD_VALUES)):
            for sv in range(len(PlayingCard.SUIT_VALUES)):
                cards.append(PlayingCard(cv, sv))

        # Empty deck
        self.card_deck = []

        # Set size of deck
        deck_size = len(PlayingCard.CARD_VALUES) * len(PlayingCard.SUIT_VALUES)

        # Shuffle
        for i in range(deck_size, 0, -1):
            rn = random.randint(0, i-1)
            self.card_deck.append(cards[rn])
            cards[rn] = cards[i-1]

    # Get the next card
    def next_card(self):
        if not self.is_empty():
            return self.card_deck.pop(0)
        return None

    # Empy deck
    def is_empty(self):
        return len(self.card_deck) == 0

# Create a player
class Player:
    # constructor
    def __init__(self, name):
        self.name = name
        self.cards = deque()  # Using deque as a queue for cards

    # add card to player's hand
    def add_card(self, card):
        self.cards.append(card)

    # play a card
    def play_card(self):
        if not self.is_empty():
            return self.cards.popleft()
        return None

    # add multiple cards to the player's hand
    def add_cards(self, card_list):
        for card in card_list:
            self.cards.append(card)

    # get how many cards there are
    def card_count(self):
        return len(self.cards)

    # set the player's hand to empty
    def is_empty(self):
        return len(self.cards) == 0

# Create the main game class
class WarGame:
    # constructor to initialize players, round, deck and shuffling and dealing of cards
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.rounds = 0
        self.deck = PlayingCardDeck()
        self.deal_cards()

    def deal_cards(self):
        # Deal 26 cards to each player
        for _ in range(26):
            self.player1.add_card(self.deck.next_card())
            self.player2.add_card(self.deck.next_card())
        print(f"Cards dealt: Player 1 has {self.player1.card_count()} cards, Player 2 has {self.player2.card_count()} cards.")


    def play_round(self):
        self.rounds += 1
        print(f"\nRound {self.rounds}:")

        # Check if either player has run out of cards
        if self.player1.is_empty():
            return "Player 2"
        elif self.player2.is_empty():
            return "Player 1"

        # Both players play a card
        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        print(f"{self.player1.name} plays {card1.card_name()}")
        print(f"{self.player2.name} plays {card2.card_name()}")

        # Pile of cards in play (for war situations)
        pile = [card1, card2]

        # Compare cards
        result = self.compare_cards(card1, card2, pile)

        return result

    def compare_cards(self, card1, card2, pile):
        if card1.playing_card_value() > card2.playing_card_value():
            print(f"{self.player1.name} wins the round!")
            self.player1.add_cards(pile)
            print(f"Player 1 now has {self.player1.card_count()} cards, Player 2 has {self.player2.card_count()} cards.")
            return None
        elif card2.playing_card_value() > card1.playing_card_value():
            print(f"{self.player2.name} wins the round!")
            self.player2.add_cards(pile)
            print(f"Player 1 now has {self.player1.card_count()} cards, Player 2 has {self.player2.card_count()} cards.")
            return None
        else:
            # War situation
            return self.handle_war(pile)

    def handle_war(self, pile):
        print("WAR!")

        # Check if either player has fewer than 4 cards (3 face down + 1 to play)
        if self.player1.card_count() < 4:
            print(f"{self.player1.name} doesn't have enough cards for war!")
            return "Player 2"
        elif self.player2.card_count() < 4:
            print(f"{self.player2.name} doesn't have enough cards for war!")
            return "Player 1"

        # Each player puts down 3 cards face down
        war_pile = pile.copy()

        print(f"{self.player1.name} puts down 3 cards face down")
        for _ in range(3):
            war_pile.append(self.player1.play_card())

        print(f"{self.player2.name} puts down 3 cards face down")
        for _ in range(3):
            war_pile.append(self.player2.play_card())

        # Play the next card for comparison
        if self.player1.is_empty() or self.player2.is_empty():
            if self.player1.is_empty() and self.player2.is_empty():
                print("Both players ran out of cards during war. It's a tie!")
                return "Tie"
            elif self.player1.is_empty():
                print(f"{self.player1.name} ran out of cards during war!")
                return "Player 2"
            else:
                print(f"{self.player2.name} ran out of cards during war!")
                return "Player 1"

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()

        print(f"{self.player1.name} plays {card1.card_name()} for war")
        print(f"{self.player2.name} plays {card2.card_name()} for war")

        war_pile.extend([card1, card2])

        # Compare the cards
        return self.compare_cards(card1, card2, war_pile)

    def play_game(self):
        print("Starting game of War!")
        winner = None

        while winner is None:
            winner = self.play_round()

            # Check if the game has gone on too long
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

# Main game execution
if __name__ == "__main__":
    game = WarGame()
    game.play_game()