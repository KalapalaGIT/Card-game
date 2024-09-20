from Cards import Deck, Card
from Player import Player

player = Player('Lassi')
deck = Deck()
deck.__init__()
player.__init__('Lassi')
# deck.shuffle()
print(deck.print_deck())
print(len(deck.cards))

player.draw(deck,50)
player.Show_hand()
print(len(deck.cards))
print(deck.print_deck())

player.draw(deck,3)
player.Show_hand()
print(f'\n{player.Show_hand()}')
player.Show_hand()

# player.draw(deck,10)
# player.draw(deck,10)
# player.draw(deck,10)
# player.Show_hand()
# print(len(player.hand))