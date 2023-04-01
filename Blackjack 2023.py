import random


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name # Name of card, i.e. Ace, King, Queen, etc.
        self.value = value # Numerical value.


suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
suitValue = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs":"\u2667", "Diamonds":"\u2662"}
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]
cardValue = {"A":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "K":10, "Q":10}


def msgDivider(msg):
    if msg == "Blackjack!":
        print("_*" * 10, end=" ")
        print(msg, end=" ")
        print("_*" * 10)
        print("\n")
    else:
        print()
        print("_" * 20, end=" ")
        print(msg, end=" ")
        print("_" * 20)
        print("\n")


def generateDeck(suits, suitValue, cards, cardValue): # Generates decks. Useful for multi-deck games.
    deck = []
    for suit in suits:
        for card in cards:
            deck.append(Card(suitValue[suit], card, cardValue[card]))

    return deck


def printCards(hand, hidden): # Prints the cards in a pretty format :>
    print(" " + "_" * 5)
    print("|", end="")
    if hidden == False:
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


def isBJ(hand):
    if hand[0].value == 11 and hand[1].value == 10:
        return True
    if hand[0].value == 10 and hand[1].value == 11:
        return True
    return False


def yesNo(choice):
    while choice.lower() not in ["y", "y.", "yes", "yes.", "n", "n.", "no", "no.", ""]:
        choice = input("Invalid input, try again: ")
    if choice.lower() in ["y", "y." "yes", "yes.", ""]:
        return True
    elif choice.lower() in ["n", "n." "no", "no."]:
        return False


def dealCard(hand, deck): # Deal card from deck, remove, returns dealt card value.
    dealtCard = random.choice(deck)
    hand.append(dealtCard)
    deck.remove(dealtCard)
    return dealtCard.value


def aces(hand, handTotal): # Prevents card total greater than 21 due to aces. Returns hand total.
    count = 0
    while handTotal > 21:
        if hand[count].value == 11:
            hand[count].value = 1
            handTotal -= 10
            count += 1
        else:
            count +=1
    return handTotal


def hit(hand, deck, choice):
    if yesNo(choice):
        dealCard(hand, deck)


def gameStart(deck):
    playerCards = []
    dealerCards = []
    playerValue = 0
    dealerValue = 0
    insurance = False

    while len(playerCards) < 2:
        playerValue += dealCard(playerCards, deck)
        dealerValue += dealCard(dealerCards, deck)
        firstCard = True
        playerValue = aces(playerCards, playerValue)
        dealerValue = aces(dealerCards, dealerValue)

        print("Player Cards: ")
        for card in playerCards:
            printCards(card, False)

        print("Dealer Cards: ") # Dealer card printout. Slightly different since one card needs to be hidden.
        for card in dealerCards:
            printCards(card, firstCard)
            if not(firstCard):
                print(f"Dealer Card: {card.value}")
            firstCard = False

        print(f"\nPlayer Total: {playerValue}\n")
        if playerValue == 21 and dealerValue != 21:
            msgDivider("Blackjack!")
            continue

        if len(dealerCards) == 2: # BJ checker; Insurance y/n
            if dealerCards[1].value == 11:
                insure = input("Would you like to purchase insurance? y/n ")
                if yesNo(insure):
                    insurance = True
                if isBJ(dealerCards):
                    print("Dealer Blackjack!")
                    if insurance:
                        print("Insurance Paid Out.")
                    else:
                        print("Insurance wasn't purchased, no payout.")
                    printCards(dealerCards[0], False)
                    printCards(dealerCards[1], False)
                    if isBJ(playerCards):
                        print("Blackjack! Push.")
                    else:
                        print("No blackjack, you lose.")
                else:
                    print("No Blackjack! No insurance payout.")
'''
If the player has Blackjack and the dealer has an Ace, they’ll be offered Even Money instead of insurance.
We’ve already learned that although it has a different name, Even Money produces the same outcome as insurance would.
Remember, if you bet £10, make Blackjack and then accept Even Money, you get £20 back for a profit of £10. If you turn
down Even Money and the dealer makes Blackjack as well, it’s a push and you get your money back.
If you turn down Even Money and the dealer doesn’t make Blackjack, you get the all-important 3 to 2 payout and make
a profit of £15. 
'''


#''' Swap between rigged and non rigged decks.

msgDivider("Welcome to Toni's BJ Lounge")
deck = generateDeck(suits, suitValue, cards, cardValue)
initialSize = len(deck)
run = True
while run:
    gameStart(deck)
    cont = input("Would you like to continue? y/n ")
    if not yesNo(cont):
        run = False
        break
    if len(deck) <= initialSize * random.uniform(.1, .25): # Reshuffle randomly between 75%-90% remains.
        msgDivider("Reshuffled Deck")
        deck = generateDeck(suits, suitValue, cards, cardValue)


# _____ Rigged Deck ______ Used for testing :>
'''
riggedCards = ["A", "10", "J", "K", "Q"]
riggedCardValue = {"A":11, "10":10, "J":10, "K":10, "Q":10}

# _____ Rigged Deck _____
msgDivider("Welcome to Toni's BJ Lounge")
riggedDeck = generateDeck(suits, suitValue, riggedCards, riggedCardValue) # Used for testing :>
initialSize = len(riggedDeck)
run = True
while run:
    gameStart(riggedDeck)
    cont = input("Would you like to continue? y/n ")
    if not yesNo(cont):
        run = False
        break
    if len(riggedDeck) <= initialSize * random.uniform(.1, .25):
        msgDivider("Reshuffled Deck")
        riggedDeck = generateDeck(suits, suitValue, riggedCards, riggedCardValue)
'''