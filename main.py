from Cards import Deck, Card
from Player import Player

player = Player('Lassi')
deck = Deck()
deck.__init__()
# deck.shuffle()
print(deck.cards)
print(len(deck.cards))

player.draw(deck,50)
print(player.hand)
print(len(deck.cards))
print(deck.cards)

player.draw(deck,3)
print(player.hand)
print(f'\n{player.hand}')
print(player.hand)

# player.draw(deck,10)
# player.draw(deck,10)
# player.draw(deck,10)
# player.Show_hand()
# print(len(player.hand))