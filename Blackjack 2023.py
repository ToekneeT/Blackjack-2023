import random


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name  # Name of card, i.e. Ace, King, Queen, etc.
        self.value = value  # Numerical value.


suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
suit_value = {
    "Spades": "\u2664",
    "Hearts": "\u2661",
    "Clubs": "\u2667",
    "Diamonds": "\u2662"}
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]
card_value = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "K": 10,
    "Q": 10}


def msg_divider(msg):
    if msg == "Blackjack!":
        print("_*" * 10, end=" ")
        print(msg, end=" ")
        print("*_" * 10)
        print("\n")
    else:
        print()
        print("_" * 20, end=" ")
        print(msg, end=" ")
        print("_" * 20)
        print("\n")


def generate_deck(suits, suit_value, cards, card_value, size):
    deck = []
    for i in range(int(size)):
        for suit in suits:
            for card in cards:
                deck.append(Card(suit_value[suit], card, card_value[card]))

    return deck


# Prints the cards in a pretty format :>
def print_cards(hand, hidden):
    print(" " + "_" * 5)
    print("|", end="")
    if not hidden:
        if hand.name == "10":
            print(hand.name, end="")
            print(" " * 3, end="|\n")
        else:
            print(hand.name, end="")
            print(" " * 4, end="|\n")
        print("|" + hand.suit + " " * 4, end="|\n")
        print("|" + " " * 5, end="|\n")
        print(" " + "-" * 5)
    else:
        print("?" + " " * 4, end="|\n")
        print("|" + " " * 5, end="|\n")
        print("|" + " " * 5, end="|\n")
        print(" " + "-" * 5)


def is_blackjack(hand):
    if hand[0].value == 11 and hand[1].value == 10:
        return True
    if hand[0].value == 10 and hand[1].value == 11:
        return True
    return False


# Returns a bool based on yes or no user input.
def yes_no(choice):
    yes_options = ["y", "y.", "yes", "yes.", ""]
    no_options = ["n", "n.", "no", "no.", "."]

    while choice.lower() not in yes_options + no_options:
        choice = input("Invalid input, try again: ")
    if choice.lower() in yes_options:
        return True
    elif choice.lower() in no_options:
        return False


# Returns a 0 if stay, 1 if hit, 2 if surrender, or 3 if double down.
def next_play(choice):
    yes_options = ["y", "y.", "yes", "yes.", ""]
    no_options = ["n", "n.", "no", "no.", "."]
    surrender_options = ["surrender", "surr"]
    hit_options = ["h", "hit"]
    dd_options = ["d", "double", "dd"]
    stay_options = ["s", "stay", "stand"]

    while choice.lower() not in yes_options + no_options + surrender_options + \
            hit_options + dd_options + stay_options:
        choice = input("Invalid input, try again: ")
    if choice.lower() in stay_options + no_options:
        return 0
    elif choice.lower() in yes_options + hit_options:
        return 1
    elif choice.lower() in surrender_options:
        return 2
    elif choice.lower() in dd_options:
        return 3


# Deal card from deck, remove, returns dealt card value.
def deal_card(hand, deck):
    dealt_card = random.choice(deck)
    hand.append(dealt_card)
    deck.remove(dealt_card)
    return dealt_card.value


# Prevents card total greater than 21 due to aces. Returns hand total.
def aces(hand, hand_total):
    count = 0
    while hand_total > 21 and count < len(hand):
        if hand[count].value == 11:
            hand[count].value = 1
            hand_total -= 10
            count += 1
        else:
            count += 1
    return hand_total


# Checks if the player wants to purchase insurance when dealer shows an Ace.
def insurance(dealer_hand, player_hand):
    # Returns 0 if dealer BJ, otherwise 1.
    if dealer_hand[1].value != 11:
        return 1

    is_player_blackjack = is_blackjack(player_hand)
    win_type = "Even Money" if is_player_blackjack else "Insurance"
    question = f"Would you like {win_type}? y/n "
    insurance = yes_no(input(question))

    if is_blackjack(dealer_hand):
        print("Dealer Blackjack!")
        print_cards(dealer_hand[0], False)
        print_cards(dealer_hand[1], False)

        payout_msg = f"{win_type} paid out." if insurance else f"{win_type} wasn't purchased, no payout."
        msg_divider(payout_msg)

        if is_player_blackjack:
            msg_divider("Blackjack! Push.")
        else:
            msg_divider("No Blackjack, you lose.")
        return 0
    else:
        msg_divider(f"No Blackjack! No {win_type} payout.")
        return 1


def surrender(dealer_hand):
    if (not is_blackjack(dealer_hand)):
        msg_divider("You surrendered your hand. Half your bet is returned.")
        return True
    return False


def double_down(player_hand, player_value, deck):
    msg_divider("You doubled your bet.")
    new_card = deal_card(player_hand, deck)
    player_value += new_card
    print_cards(player_hand[len(player_hand) - 1], False)
    player_value = aces(player_hand, player_value)
    print(f"\nPlayer Total: {player_value}\n")
    if player_value > 21:
        print("Bust!")
    return True


# Deals a card, then returns card value if yes.
def hit(hand, deck, choice):
    if yes_no(choice):
        return deal_card(hand, deck)


# Deals the player a new card, keeps asking until they either stay or bust.
def player_hit_loop(
        player_hand,
        player_value,
        dealer_hand,
        dealer_value,
        deck):
    while len(player_hand) > 2 and player_value < 21:
        print("Player Hand: ")
        for card in player_hand:
            print_cards(card, False)

        print("Dealer Hand: ")
        for i in range(len(dealer_hand)):
            if i == 0 and len(dealer_hand) <= 2:
                print_cards(dealer_hand[i], True)
            else:
                print_cards(dealer_hand[i], False)
                print(f"Dealer Card: {dealer_hand[i].value}")

        player_value = aces(player_hand, player_value)
        print(f"\nPlayer Total: {player_value}\n")
        if player_value > 21:
            msg_divider("Bust!")
            continue

        next_move = next_play(input("Hit or stay? h/s "))
        while next_move == 2 or next_move == 3:
            next_move = next_play(input("Invalid input, try again: h/s "))
        if next_move == 1:
            new_card = deal_card(player_hand, deck)
            player_value += new_card
            print_cards(player_hand[len(player_hand) - 1], False)
            player_value = aces(player_hand, player_value)
            print(f"\nPlayer Total: {player_value}\n")
            if player_value > 21:
                print("Bust!")
                continue
        elif next_move == 0:
            print("You stood.")
            dealer_hit_loop(dealer_hand, dealer_value, deck)
            winner(player_hand, player_value, dealer_hand, dealer_value)
            break  # Need to add more to this. Aka Dealer draws.
        else:  # Failsafe?
            print("You shouldn't reach this point.")


# Deals the dealer a card, keeps going until either >= 17 or bust.
def dealer_hit_loop(dealer_hand, dealer_value, deck):
    print("Dealer Hand: ")
    for card in dealer_hand:
        print_cards(card, False)
    dealer_value = aces(dealer_hand, dealer_value)
    print(f"\nDealer Total: {dealer_value}\n")

    if dealer_value < 17:
        msg_divider("The dealer will now draw.")

    while dealer_value < 17:
        new_card = deal_card(dealer_hand, deck)
        dealer_value += new_card
        for card in dealer_hand:
            print_cards(card, False)
        dealer_value = aces(dealer_hand, dealer_value)
        print(f"\nDealer Total: {dealer_value}\n")



# Determines the winner based on card values.
def winner(player_hand, player_value, dealer_hand, dealer_value):
    msg_divider("Ending Hands: ")
    print(f"Player Hand: ")
    for card in player_hand:
        print_cards(card, False)
    print(f"Dealer Hand: ")
    for card in dealer_hand:
        print_cards(card, False)
    msg_divider(f"Player Total: {player_value}")
    msg_divider(f"Dealer Total: {dealer_value}")
    if dealer_value > 21:
        msg_divider("Dealer Bust! You win!")
    elif dealer_value > player_value:
        msg_divider("Dealer wins!")
    elif dealer_value < player_value:
        msg_divider("Player wins!")


# Split Function. Separate the two cards into separate lists, or remove
# one into a new one. Act upon the two separately.


def game_start(deck):
    player_hand = []
    dealer_hand = []
    player_value = 0
    dealer_value = 0

    # Change to allow hits later (more than len of 2). Works for now due to
    # testing.
    while len(player_hand) < 2:
        player_value += deal_card(player_hand, deck)
        dealer_value += deal_card(dealer_hand, deck)
        first_card = True
        player_value = aces(player_hand, player_value)
        dealer_value = aces(dealer_hand, dealer_value)
        dd = False

        print("Player Hand: ")
        for card in player_hand:
            print_cards(card, False)

        # Dealer card printout. Slightly different since one card needs to be
        # hidden.
        print("Dealer Hand: ")
        for card in dealer_hand:
            print_cards(card, first_card)
            if not first_card:
                print(f"Dealer Card: {card.value}")
            first_card = False

        print(f"\nPlayer Total: {player_value}\n")

        # BJ Checker; Insurance y/n
        if len(dealer_hand) == 2:
            if (player_value == 21 and dealer_hand[1].value != 11) and (
                    player_value == 21 and dealer_value == 21):
                msg_divider("Dealer Blackjack; Push!")
                continue
            if (player_value == 21 and dealer_hand[1].value != 11) and (
                    player_value == 21 and dealer_value != 21):
                msg_divider("Blackjack!")
                continue
            if insurance(dealer_hand, player_hand) == 0:
                continue

            if player_value < 21:
                next_move = next_play(input("Hit or stay? h/s "))
                if next_move == 2:
                    if surrender(dealer_hand):
                        continue
                elif next_move == 1:
                    new_card = deal_card(player_hand, deck)
                    player_value += new_card
                    print_cards(player_hand[len(player_hand) - 1], False)
                    player_value = aces(player_hand, player_value)
                    print(f"\nPlayer Total: {player_value}\n")
                    if player_value > 21:
                        print("Player Hand: ")
                        for card in player_hand:
                            print_cards(card, False)
                        print(f"\nPlayer Total: {player_value}\n")
                        msg_divider("Bust!")
                        continue
                elif next_move == 3:
                    dd = double_down(player_hand, player_value, deck)
                elif next_move == 0:
                    print("You stood.")
                    dealer_hit_loop(dealer_hand, dealer_value, deck)
                    winner(player_hand, player_value, dealer_hand, dealer_value)
                    continue
                else:  # Failsafe?
                    print("You shouldn't reach this point.")

    if not dd:
        player_hit_loop(
            player_hand,
            player_value,
            dealer_hand,
            dealer_value,
            deck)
    # if dd and player_value < 21: # Dealer draws.


# ''' Swap between rigged and non rigged decks.
msg_divider("Welcome to Toni's BJ Lounge")
size = str(input("How many decks would you like to play? 1, 2, 6, or 8? "))
while size not in ["1", "2", "6", "8"]:
    size = str(input("Invalid input, try again: 1, 2, 6, or 8? "))
deck = generate_deck(suits, suit_value, cards, card_value, size)
initial_size = len(deck)
run = True

while run:
    game_start(deck)
    cont = input("Would you like to continue? y/n ")
    if not yes_no(cont):
        run = False
        break
    if int(size) != 1:
        # Reshuffle randomly between 75%-90% remains.
        if len(deck) <= initial_size * random.uniform(.1, .25):
            msg_divider("Reshuffled Deck")
            deck = generate_deck(suits, suit_value, cards, card_value, size)
    else:
        if len(deck) <= initial_size * random.uniform(.45, .55):
            msg_divider("Reshuffled Deck")
            deck = generate_deck(suits, suit_value, cards, card_value, size)

msg_divider("Thanks for playing!")


# _____ Rigged Deck ______ Used for testing :>
'''
#riggedCards = ["A", "10", "J", "K", "Q"]
riggedCards = ["A", "A", "A", "A"]
riggedCardValue = {"A":11, "10":10, "J":10, "K":10, "Q":10}

# _____ Rigged Deck _____
msg_divider("Rigged Deck Testing")
rigged_deck = generate_deck(suits, suit_value, riggedCards, riggedCardValue) # Used for testing :>
initial_size = len(rigged_deck)
run = True
while run:
    game_start(rigged_deck)
    cont = input("Would you like to continue? y/n ")
    if not yes_no(cont):
        run = False
        break
    if len(rigged_deck) <= initial_size * random.uniform(.1, .25):
        msg_divider("Reshuffled Deck")
        rigged_deck = generate_deck(suits, suit_value, riggedCards, riggedCardValue)

msg_divider("Thanks for playing!")
'''
