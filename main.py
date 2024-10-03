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
        print(f'\ncards in deck:')
        for idx, card in enumerate(reversed(self.cards)):
            print(f'{idx +1}: [{card.__str__()}]')
    
#Nostetaan kortteja
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


class Table:

    def __init__(self):
        self.cards = []
    
    def Print_table(self):
        print(f'\nCards on table:')
        for idx, card in enumerate(self.cards):
            print(f'{idx +1}: [{card.__str__()}]')

class Player:

    def __init__(self, Name):
        self.name = Name
        self.hand =[]

    def draw(self,deck: object, amount: int):
        drawn_from_deck = deck.draw_from_deck(amount)
        if drawn_from_deck:
            self.hand.extend(drawn_from_deck)
        else:
            print(f'No cards Left to draw')

    def Show_hand(self):
        print(f'\n{self.name}s cards:')
        for idx, card in enumerate(self.hand):
            print(f'{idx +1}: [{card.__str__()}]')
    
    def Place_cards(self,table: object, cards: int):
        selected_cards = []
        cards = sorted(set(cards), reverse=True)
        for index in cards:
            index -=1
            if 0 <= index < len(self.hand):
                selected_cards.append(self.hand.pop(index))
            else:
                print(f"Invalid index: {index + 1}")
        table.cards.extend(selected_cards)


# Ohjelma alkaa
def main():
    deck = Deck()
    table = Table()
    player = Player('Lassi')

    deck.shuffle()
    deck.print_deck()

    player.draw(deck,5)
    player.Show_hand()
    player.Place_cards(table,[2,4])
    table.Print_table()

main()