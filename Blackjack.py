import random


#################
#GLOBAL VARIABLES
#################

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True
current_players = 0

#############
#GAME OBJECTS
#############

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) # creates a deck of 52 card objects
    
    def __str__(self):
        deck_list = ''
        for card in self.deck:
            deck_list += '\n' + card.__str__()
        return deck_list

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop() # deals a single card

class Hand: # object for a player hand
    
    def __init__(self, num):
        self.cards = []  
        self.num = num
        self.value = 0   # start with zero hand value
        self.aces = 0    # keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        #self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips: # object for a seated player, attributes considered for chips and player
    
    def __init__(self):
        self.total = 100  # starting chip count
        self.bet = 0
        self.is_in = True # checks if player bet is still in current hand. Busting or getting blackjack leaves current hand
        self.is_playing = False # checks if player is seated to play
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

###############
#GAME FUNCTIONS
###############

def take_bet(chips): #takes bet from player
    print('Place your bet! All bets must be in increments of 5 chips.')
    print(f'Available chips: {chips.total}')
    global current_players
    if chips.total == 0:
        print("You're out of chips...")
        chips.is_playing = False
        return
    while True:
        try:
            chips.bet = int(input())
        except:
            print('Enter a number for your bet.')
        else:
            if chips.bet == 0: # player betting 0 has them exit the table and game
                chips.is_playing = False
                current_players -= 1 # Removes player from current player amount
            if chips.bet > chips.total:
                print('Not enough chips!')
                continue
            if chips.bet%5 != 0:
                print('Bets must be in increments of 5!')
                continue
            print('Bet placed.')
            break

def hit(deck,hand): #deals card to player, called in next function
    hit_card = deck.deal()
    hand.add_card(hit_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand): # asks player for game action
    global playing  # to control an upcoming while loop
    result = input('Hit or Stand?')
    if result[0].lower() == 'h':
        print('Hitting')
        hit(deck,hand)
    else:
        print('Standing')
        playing = False

def show_dealer_hidden(dealer):
    print('Dealer:')
    print('[Hidden]', dealer.cards[1])
    print('----------------------------------')

def show_dealer(dealer):
    d_hand = ''
    print('Dealer:')
    for card in dealer.cards:
        d_hand = d_hand + str(card) + ', '
    print(d_hand)
    print(f'Dealer total: {dealer.value}')
    print('----------------------------------')

def show_player(player):
    p_hand = ''
    print(f'\nPlayer {player.num}:')
    for card in player.cards:
        p_hand = p_hand + str(card) + ', '
    print(p_hand)
    print(f'Player {player.num} total: {player.value}')
    print('----------------------------------')

def show_some(player,dealer): # shown to player during game, takes Hand objects
    c_hand = ''
    print('Dealer:')
    print('[Hidden]', dealer.cards[1]) 
    print(f'\nPlayer {player.num}:')
    for card in player.cards:
        c_hand = c_hand + str(card) + ', '
    print(c_hand)
    print(f'Player {player.num} total: {player.value}')
    print('----------------------------------')
    
def show_all(player,dealer): # Shown to player after game, takes Hand objects
    c_hand = ''
    d_hand = ''
    print('Dealer:')
    for card in dealer.cards:
        d_hand = d_hand + str(card) + ', '
    print(d_hand)
    print(f'Dealer total: {dealer.value}')
    print('\nPlayer:')
    for card in player.cards:
        c_hand = c_hand
        print(card)
    print(f'Player total: {player.value}')
    print('----------------------------------')

################
#HAND CONDITIONS
################

def blackjack(chips, hand): # Checks for blackjack
    if hand.value == 21:
        print('BLACKJACK!')
        chips.win_bet()*3
        chips.is_in = False # Takes them out of current hand being played

def player_busts(chips):
    print('Busted!')
    chips.lose_bet()
    chips.is_in = False
    playing = False

def player_wins(chips, hand):
    print(f'Player {hand.num} wins a round!')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer busts!')
    chips.win_bet()
    
def dealer_wins(chips, hand):
    print(f'Dealer wins against Player {hand.num}!')
    chips.lose_bet()
    
def push(hand):
    print(f"Player {hand.value} ties with the dealer.")

##############
#PLAYER SETUP5
##############

player1 = Chips()
player2 = Chips()
player3 = Chips()
player4 = Chips()
player5 = Chips()
player6 = Chips()
player7 = Chips()

# Iterable dict of player/chip objects with numbered keys
player_list = {1 : player1, 2 : player2, 3 :player3, 4 : player4,
            5 : player5, 6 : player6, 7 : player7}

# Check how many are playing
while True:
    try:
        total_players = int(input('How many players are starting?'))
    except:
        print('Enter a number')
        continue
    else:
        if total_players > 7 or total_players < 0:
            print('Player number must be between 1 and 7')
            continue
        for n in range(1,total_players+1):
            player_list.get(n).is_playing = True # Iterate through dict to return Chips object at key n
        break

current_players = total_players # Tracks players still in the game 

###########
#GAME START
###########

while True: # Game is running
    print('Beginning game!')
     
    # Create and shuffle the deck
    new_deck = Deck()
    if current_players > 3:
        second_deck = Deck()
        new_deck.deck.extend(second_deck.deck) # Add a second 52 card deck if more than 3 players
    new_deck.shuffle()
    
    # Initialize hands
    player1_hand = Hand(1)
    player2_hand = Hand(2)
    player3_hand = Hand(3)
    player4_hand = Hand(4)
    player5_hand = Hand(5)
    player6_hand = Hand(6)
    player7_hand = Hand(7)
    dealer = Hand(0)

    # Iterable dict of player hand objects with numbered keys
    hand_list = {1 : player1_hand, 2 : player2_hand, 3 : player3_hand, 4 : player4_hand,
                5 : player5_hand, 6 : player6_hand, 7 : player7_hand}

    # Prompt the Players for their bets
    for n in range(1,total_players+1):
        if player_list.get(n).is_playing == True: # Check if player is seated to bet 
            print(f'Player {n}:')
            take_bet(player_list.get(n))
            if player_list.get(n).bet == 0: # take_bet sets is_playing attribute to False
                print(f'Goodbye Player {n}!')
                current_players -= 1 

    # Deal cards to players in the game
    if player1.is_playing == True:
        player1_hand.add_card(new_deck.deal())
        player1_hand.add_card(new_deck.deal())
    
    if player2.is_playing == True:
        player2_hand.add_card(new_deck.deal())
        player2_hand.add_card(new_deck.deal()) 

    if player3.is_playing == True:
        player3_hand.add_card(new_deck.deal())
        player3_hand.add_card(new_deck.deal())
    
    if player4.is_playing == True:
        player4_hand.add_card(new_deck.deal())
        player4_hand.add_card(new_deck.deal())

    if player5.is_playing == True:
        player5_hand.add_card(new_deck.deal())
        player5_hand.add_card(new_deck.deal())

    if player6.is_playing == True:
        player6_hand.add_card(new_deck.deal())
        player6_hand.add_card(new_deck.deal())

    if player7.is_playing == True:
        player7_hand.add_card(new_deck.deal())
        player7_hand.add_card(new_deck.deal())
   
    # Deal cards to dealer
    dealer.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    
    # Show cards (but keep one dealer card hidden) and check for Blackjack
    show_dealer_hidden(dealer)
    for n in range(1,total_players+1):
        if player_list.get(n).is_playing == True: 
            show_player(hand_list.get(n))
            blackjack(hand_list.get(n)) # Iterate through dict to return Hand object at key n

    # Loop for player round
    while True:  
        # Prompt for Players to Hit or Stand
        for n in range(1,total_players+1):
            playing = True # Global variable checking if player is hitting/standing
            while playing:
                if (player_list.get(n).is_playing and player_list.get(n).is_in) == True and hand_list.get(n).cards < 5: 
                    hit_or_stand(new_deck,hand_list.get(n))
                    show_dealer_hidden(dealer)
                    show_player(hand_list.get(n))
                    ###show_some(hand_list.get(n),dealer)
                    if hand_list.get(n).value > 21:
                        player_busts(player_list.get(n))
                playing = False
                break
        break
    
    # Loop for dealer round
    while dealer.value < 17: # Dealer hits if their hand value is less than 17
        if len(dealer.cards) < 5:
            hit(new_deck, dealer)
            continue  
        break

    # Check player hands to dealer
    if dealer.value > 21 and current_players > 0: # Dealer busts, players still in the hand win bet
        show_dealer(dealer)
        print('Dealer busts!')
        for n in range(1,total_players+1):
            if player_list.get(n).is_playing and player_list.get(n).is_in:
                player_list.get(n).win_bet()
    else:
        for n in range(1,total_players+1): # Compare hand values with dealer and decide winning bets
            if player_list.get(n).is_playing and player_list.get(n).is_in:
                show_dealer(dealer)
                show_player(hand_list.get(n))
                if hand_list.get(n).value > dealer.value:
                    player_wins(player_list.get(n), hand_list.get(n))
                elif hand_list.get(n).value < dealer.value:
                    dealer_wins(player_list.get(n), hand_list.get(n))
                else:
                    push(hand_list.get(n))

    # Inform Players of their chips total
    print('-'*15)
    for n in range(1,total_players+1):
        if player_list.get(n).is_playing:
            print(f'-Player {n}: {player_list.get(n).total}-')
    print('-'*15)
  
    # Ask to play again
    if current_players > 0:
        retry = input('New round? (y/n)')
        if retry[0].lower() == 'y':
            playing = True
            continue
                
    print('Game end')
    
    break