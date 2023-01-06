# Card class
# containing suit, rank, value
# Deck
import random
suits = ('Hearts','Spades','Clubs','Diamonds')
ranks = ('Two', 'Three', 'Four','Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
playing = True
class Card:
    
    def __init__ (self, suit, rank):
        self.rank = rank
        self.suit = suit
        self.value = values[self.rank]
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: "+ deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_for_ace(self):
        # if total value is over 21, and there is an ace, then ace = 1, not 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
class Chips:
    
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
def take_bet(chips):
    
    while True:
        
        try:
            print("How many chips would you like to bet?")
            chips.bet = int(input())
        except:
            print("\nInput an integer")
        else:
            if chips.bet > chips.total:
                print("\nBet exceeds availiable balance!")
            else:
                break
def hit(deck, hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
def hit_or_stand(deck, hand):
    
    global playing
    
    while True:
        x = input("Hit or Stand? Enter h or s.")
        
        if x[0].lower() == 'h':
            hit(deck, hand)
        
        elif x[0].lower() == 's':
            print("Player Stands, Dealer's Turn")
            playing = False
        
        else:
            print("Enter h or s.")
            continue
        break
def show_some(player, dealer):
    # Show only one of dealer's cards
    print("\n Dealer's Hand: ")
    print("First Card Hidden!")
    print(dealer.cards[1])
    
    # Show all player's cards:
    print("\n Player's cards: ", *player.cards, sep = "\n")
    print("Player's total: ",player.value)
def show_all(player, dealer):
    # show all dealer's cards and their cumalative value
    print("\n Dealer's Hand: ", *dealer.cards, sep = "\n")
    print(f"Value of Dealer's Hand is: {dealer.value}.")
    # Show all player's cards:
    print("\n Player's cards: ", *player.cards, sep = "\n")
    print(f"Value of Player's Hand is: {player.value}.")
def player_busts(player, dealer, chips):
    print("Bust Player!")
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print("Player Wins!")
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print("Player Wins! Dealer Busted!")
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print("Dealer Wins!")
    chips.lose_bet()
def push(player, dealer):
    print("Dealer and Player tie! Push!")
while True:
    # Print opening statement
    print("Welcome to BlackJack!")
    
    # Create a new shuffled deck of 52 cards
    deck = Deck()
    deck.shuffle()
    
    # Deal 2 cards to the player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    # 2 cards to the dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Provide player with chips
    player_chips = Chips()
    
    # Ask player for their bet
    take_bet(player_chips)
    
    # Show one card of the dealer and all the cards of the player
    show_some(player_hand, dealer_hand)
    
    
    while playing:
        
        # Ask if player wants to hit or stand
        hit_or_stand(deck, player_hand)
        
        # Show one card of dealer and all of the player's
        show_some(player_hand, dealer_hand)
        
        # If player hand exceeds 21, player is busted, subtract bet from chips
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
            
    # If player hasn't busted and deal cards for dealer until value is 17
    if player_hand.value < 21:
        
        while dealer_hand.value < 17: # or player_hand.value
            hit(deck, dealer_hand)
            
        # Show all cards
        show_all(player_hand, dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value > player_hand.value: 
            dealer_wins(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
            
    # Inform player of their balance
    print("\n Player total chips are at: {}".format(player_chips.total))
    
    # Ask to play again
    new_game = input("Want to continue? Y/n")
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    
    else:
        print("Thank You for playing!")
        break
