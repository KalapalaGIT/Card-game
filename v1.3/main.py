import random
from abc import ABCMeta
import time

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Aseta testiajo tästä
TEST_MODE = False

#Kortti luokka
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
    
# Poistopakka
class DeletedCards(Deck):
    def __init__(self):
        super().__init__()
        self.cards = []


# Pelattava pöytä
class Table():
    def __init__(self):
        self.cards = []
    
    # Tulostaa kaikki pöydällä olevat kortit
    def Print_table(self):
        print(f'\nCards on table:')
        for idx, card in enumerate(self.cards):
            print(f'{idx +1}: [{card.__str__()}]')

    # Ottaa vastaan pelaajan laittamat kortit
    def take_cards(self, input_cards):
        self.cards.extend(input_cards)


# Tulostaa viimeisimmän kortin pöydällä
    def Print_latest_card(self):
        if self.cards:
            print(f"\nLast card on table:")
            try:
                print(f"[{self.cards[-1].__str__()}]")
            except:
                print("ERROR: Cannot show cards.")

        else:
            print("No cards on the table.\n")
    
# Palauttaa viimeisimmän kortin arvo
    def latest_card_value(self):
        if self.cards:
            return self.cards[-1].get_value()
        else:
            return 0


# Pelaaja luokka
class Player(metaclass=ABCMeta):

    def __init__(self, Name):
        self.name = Name
        self.hand =[]

    def GetName(self):
        return self.name

# Nostaa pakasta kortteja halutun määrän
    def draw(self,deck: object, amount: int):
        drawn_from_deck = deck.draw_from_deck(amount)
        if drawn_from_deck:
            self.hand.extend(drawn_from_deck)
        else:
            print(f'\nNo cards Left to draw')


# Tulostaa pelaajan kädessä olevat kortit
    def Show_hand(self):
        print(f'\n{self.name}s cards:')
        for idx, card in enumerate(self.hand):
            print(f'{idx +1}: [{card.__str__()}]')


# Laittaa pöydälle indexillä valitut kortit
    def Place_cards(self,table: object, cards: int):
        selected_cards = []
        cards = sorted(set(cards), reverse=True)
        print("\nPlaced cards:")
        for index in cards:
            if 0 <= index < len(self.hand):
                card = self.hand[index]
                print(f"[{card.__str__()}]")
                selected_cards.append(self.hand.pop(index))
            else:
                print(f"\nInvalid index: {index + 1}")
        table.take_cards(selected_cards)


# Teksi- ja AI pelaajaluokat
class TextPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

class AI_Player(Player):
    def __init__(self, name, cards_on_table, deletedCards):
        super().__init__(name)
        self.hand = []
        self.cards_on_table = cards_on_table
        self.deletedCards = deletedCards


# Pelitilanne pelin tilanteen arviointia varten
class Status:
    def __init__(self, test_mode):
        self.current_turn = 0
        self.history = []
        self.players = []
        self.test_mode = test_mode


    # Kutsuu pelin aloittajan arvontaa
    def decide_starting(self):
        starter = StartingPlayer.starting_player(self.players)
        self.current_turn = self.players.index(starter)

    # Asetetaan pelin asetukset (Pelaajien lukumäärä, ja pelaajien nimet.)
    def setup_game(self, deck):

        # Ohittaa pelin asetuksien asettelun (Testiajo)
        if self.test_mode:
            print("Test mode activated. Deactivate flag in Status.setup_game().")
            self.players.append(TextPlayer("Sini"))
            self.players.append(TextPlayer("Lassi"))
            self.players.append(TextPlayer("Toni"))
            for player in self.players:
                player.draw(deck, 5)
            deck.cards = deck.cards[:10]
            return
        
        # Pelin asetuksien asettelu
        while True:
            try:
                num_players = int(input("Enter the number of players (2-10): "))
                if 2 <= num_players <= 10:
                    break
                else:
                    print("Please enter a number between 2 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        for i in range(num_players):
            name = input(f"Enter name for player {i + 1}: ").strip()
            player = TextPlayer(name)
            player.draw(deck, 5)
            self.players.append(player)
        print("\nPlayers are ready")


    # Aihio korttien pelaamista varten
    def place_cards(self, player):
        card_input = input("Input the card numbers you want to place (e.g. '2,3' or '1')\nCards: ")
        
        try:
            card_indices = [int(x.strip()) -1 for x in card_input.split(",")]
            
            if all(0 <= index < len(player.hand) for index in card_indices):
                card_values = [player.hand[index].get_value() for index in card_indices]
                    
                if len(set(card_values)) == 1:
                    player.Place_cards(self.table, [index for index in card_indices])
           
                    for index in card_indices:
                        card = player.hand[index]
                    
                else:
                    print("\nERROR: All selected cards must have the same value.\n")
            else:
                print("\nERROR: Invalid card index(es) provided.\n")
        except ValueError:
            print("\nERROR: Wrong format. Input only number(s) separated by a comma. (e.g. 4,9,1)\n")
    
    # Palauttaa vuorossa olevan pelaajan
    def get_current_player(self):
        return self.players[self.current_turn]
    
    # Antaa vuoron seuraavalle pelaajalle
    def toggle_turn(self):
        self.current_turn = (self.current_turn + 1) %len(self.players)

# Judge luokka määrittää pelin säännöt
class Judge:
    
    # Tarkistaa onko pelaajan siirto sääntöjen mukainen
    @classmethod
    def validate_move(self, table, played_cards):
        
        if all(card.GetRank() == played_cards[0].GetRank() for card in played_cards):   # Kaikilla korteilla sama arvo
            
            if not table.cards:  # Tyhjä pöytä
                return True

            if not played_cards:
                return False  
        
            played_value = played_cards[0].get_value()
            last_value = table.latest_card_value()

            match played_value:

            # Kymppikortin tarkistus
                case 10:
                    if played_value == 10 and last_value <= 10:
                        return True
                    return False
            # ässän tarkistus
                case 14:
                    if played_value == 14 and 15 > last_value >= 11:
                        return True
                    return False
            # Ettei laitettava kortti ole pienempi
                case _:
                    if played_value >= last_value:
                        return True
                    return False
        return False

    # Päivittää pelitilanteen (pakan kaatuminen, korttien nostaminen)
    @classmethod
    def update_game_state(self, table, deletedCards, played_cards, status, player):
        
        match played_cards[0].get_value():

            # Kortti 10 kaataa pakan
            case 10:
                print("\nThe pile collapses due to a 10! The current player keeps the turn.")
                time.sleep(1)
                deletedCards.cards.extend(table.cards)
                table.cards.clear()
                return True # Vuoro ei vaihdu

            # Kortti 14 (ässä) kaataa pakan
            case 14:
                print("\nThe pile collapses due to an Ace! The current player keeps the turn.")
                time.sleep(1)
                deletedCards.cards.extend(table.cards)
                table.cards.clear()
                return True # Vuoro ei vaihdu

            # Kortti 2 vain korttien 2 päälle
            case 15:
                if played_cards[0].get_value() != 15:
                    print("\nERROR: 2 can only be placed on another 2.")
                    time.sleep(1)
                    return False
                
            # Jos mikään ei täyty vuoro vaihtuu
            case _: False

    # Tarkistaa onko pelaajalla kelvollisia kortteja
    @classmethod
    def has_valid_move(self, table, player):
        if not table.cards:  # Pöytä on tyhjä, mikä tahansa kortti käy
            return True

        # tarkistaa jokaisen kortin yksitellen
        for card in player.hand:
            if self.validate_move(table, [card]):
                return True

        return False

    # Pelaaja nostaa pöydän kortit, jos ei voi tehdä siirtoa
    @classmethod
    def handle_no_valid_move(self, table, deletedCards, player):
        if not self.has_valid_move(table, player):
            print(f"\n{player.name} cannot play any card and must pick up the pile!")
            player.hand.extend(table.cards)
            table.cards.clear()
            time.sleep(1)
            return True
        return False
    
    # Nostaa automaattisesti pelaajalle kortteja vuoron jälkeen
    @classmethod
    def handle_card_pick(self, deck, player):
        if deck.cards and len(player.hand) < 5:
            amount = 5 - len(player.hand)
            player.draw(deck, amount)
            print(f"\ncards left in deck: {len(deck.cards)}")
            if not deck.cards:
                print("\nDeck is empy. All cards are distributed")
                time.sleep(2)
        return
            

# Pelitilanne pelin tilanteen arviointia varten
# Aloittavan pelaajan arvonta
class StartingPlayer:
    @staticmethod
    # Hae pelaajien kädestä pienin kortti: 3->
    def starting_player(players):
        smallest_card_value = [(player, min(card.get_value() for card in player.hand)) for player in players]
        starter = min(smallest_card_value, key=lambda x: x[1])[0]
        return starter 

# Hoitaa pelin toiminnallisuuden  
class GameMenu:
    def __init__(self, status, table, deletedCards):
        self.status = status
        self.table = table
        self.deletedCards = deletedCards
        self.deck = Deck()
        self.judge = Judge()
        self.starting_player = StartingPlayer()
        self.place = 1  

    def Check_Winner(self,deck, player):
        if not deck.cards and not player.hand:
            return True
    def handle_winner(self, player):
        if self.place == 1:
            print(f"\n{player.name} wins!")
            self.place +=1
        else:
            print(f"\n{player.name} finished at {self.place}. place")
            self.place +=1
        self.status.players.remove(player)
        self.status.toggle_turn()

        if len(self.status.players) == 1:
            print(f"Game over!\n{self.status.players[0].name} on paskahousu")
            exit()

    def start_game(self):
        if not self.status.players:
            self.setup_game()

        self.status.decide_starting()
            
        print("\nStarting the game!")
        while True:
            current_player = self.status.get_current_player()
            action = self.display_turn_menu(current_player)
            self.handle_action(action, current_player)
            
    # Pelin aloitus   
    def setup_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.status.setup_game(self.deck)

    def display_turn_menu(self, player):
        time.sleep(1)
        print(f"\n{player.name}'s turn.\nWhat do you want to do next?\n[1] Show my deck\n[2] Place card(s)\n[3] Show the table\n")
        return input("Choose: ")

    def handle_action(self, action, player):
        try:
            # Näytä oma käsi
            if action == '1':
                player.Show_hand()
                return 
            
            # Pelaa kortti(/kortteja)
            elif action == '2':
                if self.judge.handle_no_valid_move(self.table,self.deletedCards, player):
                    # Pelaaja nosti kortit eikä voi jatkaa
                    self.status.toggle_turn()
                    return
                
                self.table.Print_latest_card()
                player.Show_hand()

                card_indices = input("Enter card indices to play (e.g. '1,2'): ").strip()
                card_indices = [int(idx) - 1 for idx in card_indices.split(",")]

                played_cards = [player.hand[idx] for idx in card_indices]

                if self.judge.validate_move(self.table, played_cards):
                    player.Place_cards(self.table, card_indices)
                    self.judge.handle_card_pick(self.deck, player)

                    if self.Check_Winner(self.deck, player):
                        self.handle_winner(player)
                        self.status.toggle_turn()
                        return
                    
                    if not self.judge.update_game_state(self.table, self.deletedCards, played_cards, self.status, player):
                        # Jos vuoro ei pysy pelaajalla, vaihda vuoroa
                        self.status.toggle_turn()
                else:
                    print("\nInvalid move. Try again.")

            # Näytä pöydän ylin kortti
            elif action == '3':
                self.table.Print_latest_card()
                return  
        except Exception as e:
            print(f"ERROR: An error has occurred. {e}")



# Ohjelma alkaa
def main():

    table = Table()
    status = Status(test_mode=False)
    deleted_cards = DeletedCards()
    
    # Aloittaa pelin
    game_menu = GameMenu(status, table, deleted_cards)
    game_menu.start_game()
    
main()