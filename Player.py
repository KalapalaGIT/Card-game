from Cards import Deck

deck = Deck()

class Player:

    def __init__(self, Name):
        self.name = Name
        self.hand =[]

    def draw(self,deck, amount):
        drawn_from_deck = deck.draw_from_deck(amount)
        if drawn_from_deck:
            for card in drawn_from_deck:
                self.hand.append(card)
        else:
            print(f'No cards Left for {self.name} to draw. {len(drawn_from_deck)} cards drawn.')

    def Show_hand(self):
        for card in self.hand:
            print(card)