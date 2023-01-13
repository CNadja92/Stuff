import random

#GLOBAL VARIABLES
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


#GAME OBJECTS
class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card) # creates a deck of 52 card objects
    
    def __str__(self):
        deck_list = ''
        for card in self.deck:
            deck_list += '\n' + card.__str__()
        return deck_list

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop() # deals a single card

class Hand:
    
    def __init__(self):
        self.cards = []  
        self.value = 0   # start with zero hand value
        self.aces = 0    # keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self):
        self.total = 100  # starting chip count
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#GAME FUNCTIONS
def take_bet(chips): #takes bet from player
    print('Place your bet!')
    print(f'Available chips: {chips.total}')
    while True:
        
        try:
            chips.bet = int(input())
    
        except:
            print('Enter a number for your bet.')
        else:
            if chips.bet <= chips.total:
                print('Bet placed!')
                break
            else:
                print('Not enough chips.')

def hit(deck,hand): #deals card to player, called in next function
    hit_card = deck.deal()
    hand.add_card(hit_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand): #asks player for game action
    global playing  # to control an upcoming while loop
    print('Hit or Stand?')
    while True:
        result = input()
        if result == 'Hit':
            print('Hitting')
            hit(deck,hand)
        elif result == 'Stand':
            print('Standing')
            playing = False
        else:
            print('Select an option')
            continue
        break

def show_some(player,dealer): #shown to player during game
    print('Dealer:')
    print('[Hidden]')
    print(dealer.cards[1])   
    print('\nPlayer:')
    for card in player.cards:
        print(card)
    print(f'Player total: {player.value}')
    print('----------------------------------')
    
def show_all(player,dealer): #shown to player after game
    print('Dealer:')
    for card in dealer.cards:
        print(card)
    print(f'Dealer total: {dealer.value}')
    print('\nPlayer:')
    for card in player.cards:
        print(card)
    print(f'Player total: {player.value}')
    print('----------------------------------')

#GAME END CONDITIONS
def player_busts(chips):
    print('Busted!')
    chips.lose_bet()
    playing = False

def player_wins(chips):
    print('Player wins!')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer busts!')
    chips.win_bet()
    
def dealer_wins(chips):
    print('Dealer wins!')
    chips.lose_bet()
    
def push():
    print("It's a tie.")

#GAME START
player_chips = Chips()
while True:
    # Print an opening statement
    print('Blackjack!')
    
    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()
    
    player = Hand()
    dealer = Hand()
    
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        if len(player.cards) < 5:
            hit_or_stand(new_deck,player)
        
            # Show cards (but keep one dealer card hidden)
            show_some(player,dealer)
        
            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player.value > 21:
                player_busts(player_chips)
                show_all(player,dealer)
                break
        else:
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        while dealer.value < 17:
            if len(dealer.cards) < 5:
                hit(new_deck,dealer)
                continue
            break
        # Show all cards
        show_all(player,dealer)
        # Run different winning scenarios
        if dealer.value > 21:
            dealer_busts(player_chips)
        else:
            if player.value == dealer.value:
                push()
            elif player.value > dealer.value:
                player_wins(player_chips)
            else:
                dealer_wins(player_chips)
                
    
    # Inform Player of their chips total 
    print(f'Current chips: {player_chips.total}')
    
    
    # Ask to play again
    if player_chips.total > 0:
        retry = input('Play again? (y/n)')
        if retry[0].lower() == 'y':
            playing = True
            continue
                
    print('Game end')
            
    break