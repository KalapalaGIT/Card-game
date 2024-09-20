import random

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if self.suit == 'Hearts' or self.suit == 'Diamonds':
            self.color = 'Red'

        else:
            self.color = 'Black'

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return self.__str__()

# Palauttaa kortin arvon numerona.
    def get_value(self):
        if self.rank == 'J':
            return 11
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'K':
            return 13
        elif self.rank == 'A':
            return 1
        else:
            return int(self.rank)

# Luodaan Pakka
class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

# Sekoitetaan pakan järjestys
    def shuffle(self):
        random.shuffle(self.cards)

    def print_deck(self):
        for card in self.cards:
            print(card)
    
    def draw_from_deck(self, amount):
        drawn = []
        for _ in range(amount):
            if len(self.cards)>0:
                card = self.cards.pop()
                drawn.append(card)
            else:
                print('Deck is empty')
                break
        return drawn
