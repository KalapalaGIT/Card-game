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
    
    def GetColor(self):
        return self.color
    
    def GetSuit(self):
        return self.suit
    
    def GetRank(self):
        return self.rank 

# Palauttaa kortin arvon numerona.
    def get_value(self):
        if self.rank == 'J':
            return 11
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'K':
            return 13
        elif self.rank == 'A':
            return 14
        elif self.rank == '2':
            return 15
        else:
            return int(self.rank)

# Palauttaa korttien vertailun 
    # ==
    def __eq__(self,other):
        if  Card.get_value(self) == Card.get_value(other):
            return True
        else:
            return False
    # >=
    def __ge__(self,other):
        if  Card.get_value(self) >= Card.get_value(other):
            return True
        else:
            return False
    # <=
    def __le__(self,other):
        if  Card.get_value(self) <= Card.get_value(other):
            return True
        else:
            return False
    # <
    def __lt__(self,other):
        if  Card.get_value(self) < Card.get_value(other):
            return True
        else:
            return False
    # >
    def __gt__(self,other):
        if  Card.get_value(self) > Card.get_value(other):
            return True
        else:
            return False
    # !=
    def __ne__(self,other):
        if  Card.get_value(self) != Card.get_value(other):
            return True
        else:
            return False

# Luodaan Pakka
class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffleled = False

    def __str__(self):
        cards_str = "\n".join(f"{index+1}: {card.rank} of {card.suit}" for index, card in enumerate(reversed(self.cards)))
        return f'\nCards in deck:\n{cards_str}'

# Sekoitetaan pakan järjestys
    def shuffle(self):
        random.shuffle(self.cards)
        self.shuffleled = True

# Tulostetaan pakassa olevat kortit
    def print_deck(self):
        if self.shuffleled:   
            print(f'\ncards in deck:')
            for idx, card in enumerate(reversed(self.cards)):
                print(f'{idx +1}: {card.__str__()}')
        else:
            self.shuffle()
            self.print_deck()
    
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
    
# Tulostaa kaikki pöydällä olevat kortit
    def Print_table(self):
        print(f'\nCards on table:')
        for idx, card in enumerate(self.cards):
            print(f'{idx +1}: [{card.__str__()}]')

# Tulostaa viimeisimmän kortin pöydällä
    def Print_card(self):
        if self.cards:
            print(f"\nLast card on table:")
            try:
                print(f"[{self.cards[-1].__str__()}]")
            except:
                print("ERROR: Cannot show cards.")

        else:
            print("No cards on the table.\n")

    def latest_card_value(self):
        if self.cards:
            return self.cards[-1].get_value()
        else:
            return 0

# Pelaaja luokka
class Player:

    def __init__(self, Name):
        self.name = Name
        self.hand =[]

# Nostaa pakasta kortteja halutun määrän
    def draw(self,deck: object, amount: int):
        drawn_from_deck = deck.draw_from_deck(amount)
        if drawn_from_deck:
            self.hand.extend(drawn_from_deck)
        else:
            print(f'No cards Left to draw')

# Tulostaa pelaajan kädessä olevat kortit
    def Show_hand(self):
        print(f'\n{self.name}s cards:')
        for idx, card in enumerate(self.hand):
            print(f'{idx +1}: [{card.__str__()}]')

# Laittaa pöydälle indexillä valitut kortit
    def Place_cards(self,table: object, cards: int):
        selected_cards = []
        cards = sorted(set(cards), reverse=True)
        for index in cards:
            if 0 <= index < len(self.hand):
                card = self.hand[index]
                print(f"Placed cards: {index + 1} : [{card.__str__()}]")
                selected_cards.append(self.hand.pop(index))
            else:
                print(f"Invalid index: {index + 1}")
        table.cards.extend(selected_cards)

# Aloittavan pelaajan arvonta
class StartingPlayerSelector:
    @staticmethod
    # Hae pelaajien kädestä pienin kortti: 3->
    def get_smallest_card_value(player):
        return min(card.get_value() for card in player.hand)

    # Tarkastele kummalla on seuraavaksi pienin kortti
    @staticmethod
    def determine_starting_player(player1, player2):
        for value in range(4, 15):
            player1_has_value = any(card.get_value() == value for card in player1.hand)
            player2_has_value = any(card.get_value() == value for card in player2.hand)
            if player1_has_value and not player2_has_value:
                return player1
            elif player2_has_value and not player1_has_value:
                return player2
        return player1

    @staticmethod
    # Päätä, kumpi pelaajista aloittaa
    def decide_starting_turn(player1, player2):
        player1_smallest = StartingPlayerSelector.get_smallest_card_value(player1)
        player2_smallest = StartingPlayerSelector.get_smallest_card_value(player2)
        # Katso, kummalla pelaajista on pienempi kortti
        if  player1_smallest < player2_smallest:
            return player1, 1
        # Jos kumallakin pelaajalla on pienin kortti, katso seuraavaksi pienin
        elif player1_smallest == player2_smallest:
            next_player = StartingPlayerSelector.determine_starting_player(player1, player2)
            return next_player, 1 if next_player == player1 else 2
        else:
            return player2, 2

class GameMenu:
    def __init__(self, player1, player2, table, deck):
        self.player1 = player1
        self.player2 = player2
        self.table = table
        self.deck = deck
        self.turn = None
        self.card_placed = False

    def display_turn_menu(self, player):
        print(f"\n{player.name}'s turn.\nWhat do you want to do next?\n[1] Show my deck\n[2] Place card(s)\n[3] Draw a card\n[4] Show the table\n[5] End turn\n")
        return input("Choose: ")

    def handle_action(self, action, player):
        try:
            # Näytä oma käsi
            if action == '1':
                player.Show_hand()
            # Pelaa kortti(/kortteja)
            elif action == '2':
                self.place_cards(player)
            # Nosta kortti
            elif action == '3':
                self.draw_cards(player)
            # Näytä pöydän ylin kortti
            elif action == '4':
                self.table.Print_card()
            # Lopeta vuoro
            elif action == '5':
                self.toggle_turn(player)
                self.placed_cards = False
        # Vikatilanteiden selvittämistä varten
        except Exception as e:
            print(f"ERROR: An error has occurred. {e}")

    def place_cards(self, player):
        card_input = input("Input the card numbers you want to place (e.g. '2,3' or '1')\nCards: ")
        
        try:
            card_indices = [int(x.strip()) -1 for x in card_input.split(",")]
            
            # Onko oikeat indexit annettu
            if all(0 <= index < len(player.hand) for index in card_indices):
                card_values = [player.hand[index].get_value() for index in card_indices]

                # onko korttien arvot samat     
                if len(set(card_values)) == 1:

                    # Laitettavian korttien ja pöydän korttien vertailu
                    if not self.table.cards or card_values[0] >= self.table.latest_card_value():
                        player.Place_cards(self.table, [index for index in card_indices])
                        self.card_placed = True
   
                        for index in card_indices:
                            card = player.hand[index]
                    else:
                        print("\nERROR: Selected cards must be higher or equal to the card on the table.\n")
    

                else:
                    print("\nERROR: All selected cards must have the same value.\n")
            else:
                print("\nERROR: Invalid card index(es) provided.\n")
        except ValueError:
            print("\nERROR: Wrong format. Input only number(s) separated by a comma. (e.g. 4,9,1)\n")

    def draw_cards(self, player):

        if self.deck.cards:
            while len(player.hand) < 5 and self.deck.cards:
                player.draw(self.deck, 1)
            print(f"{player.name} drew cards from deck")
        else:
            print(f"{player.name} Drawing the entire table!")
            self.handle_no_placement(player)

    def check_no_placement(self, player):
        """Check if the player can place at least one card."""
        if self.card_placed:
            return False # Player has least one card placed
        elif not self.table.cards:
            return False  # If the table is empty, any card can be placed.

        top_card_value = self.table.cards[-1].get_value()
        for card in player.hand:
            if card.get_value() >= top_card_value:
                return False  # Player has at least one valid card to place.
        return True  # No valid card to place.

    def handle_no_placement(self, player):
        """If the player cannot place any cards, they draw the table."""
        print(f"{player.name} cannot place any cards and will draw the table!")
        player.hand.extend(self.table.cards)
        self.table.cards = []  # Clear the table after drawing.
    
    def toggle_turn(self, player):
        if self.check_no_placement(player):
            self.handle_no_placement(player)
        self.turn = 2 if self.turn == 1 else 1
        self.card_placed = False
        print(self.card_placed)

    def start_game(self):
        starter, turn = StartingPlayerSelector.decide_starting_turn(self.player1, self.player2)
        #print(f"Player {starter.name} has the smallest card and will go first.")
        self.turn = turn

        while True:
            current_player = self.player1 if self.turn == 1 else self.player2
            
            action = self.display_turn_menu(current_player)
            self.handle_action(action, current_player)


# Ohjelma alkaa
def main():
    deck = Deck()
    table = Table()

    # Sekoita kortit
    deck.shuffle()
    # Näytä koko pakka
    #deck.print_deck() 

    # Pelaajien luonnin automatisointi testaamisen nopeuttamiseksi
    player1 = Player("Sini")
    player2 = Player("Lassi")

    player1.draw(deck,5)
    player2.draw(deck,5)

    player1.Show_hand()
    player2.Show_hand()
    #player.draw(deck,5)
    #player.Show_hand()
    #player.Place_cards(table,[2,4])
    table.Print_table()

    # Arvotaan kumpi pelaajista aloittaa
    starting_player, turn = StartingPlayerSelector.decide_starting_turn(player1, player2)
    print(f"Player {starting_player.name} has the smallest card and will go first.")

    game_menu = GameMenu(player1, player2, table, deck)
    game_menu.turn = turn
    game_menu.start_game()


main()
