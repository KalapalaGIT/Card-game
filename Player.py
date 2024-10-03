from Cards import Deck

deck = Deck()

class Player:

    def __init__(self, Name):
        self.name = Name
        self.hand =[]

    def draw(self,deck, amount):
        drawn_from_deck = deck.draw_from_deck(amount)
        if drawn_from_deck:
            self.hand.extend(drawn_from_deck)
        else:
            print(f'No cards Left to draw')

    def Show_hand(self):
        for idx, card in enumerate(self.hand):
            print(f'{idx +1}: [{card.__str__()}]')