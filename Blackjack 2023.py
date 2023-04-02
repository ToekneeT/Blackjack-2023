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
        print("*_" * 10)
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


def yesNo(choice): # Returns a bool based on yes or no user input.
    while choice.lower() not in ["y", "y.", "yes", "yes.", "n", "n.", "no", "no.", ""]:
        choice = input("Invalid input, try again: ")
    if choice.lower() in ["y", "y." "yes", "yes.", ""]:
        return True
    elif choice.lower() in ["n", "n." "no", "no."]:
        return False


def nextPlay(choice): # Returns a 0 if stay, 1 if hit, or 2 if surrender.
    while choice.lower() not in ["surr", "stay", "s", "surrender", "give up", "g", "h", "hit",
    "y", "y.", "yes", "yes.", "n", "n.", "no", "no.", ""]:
        choice = input("Invalid input, try again: ")
    if choice.lower() in ["h", "hit", "y", "y.", "yes", "yes.", ""]:
        return 1
    elif choice.lower() in ["stay", "s", "n", "n.", "no", "no."]:
        return 0
    elif choice.lower() in ["surr", "surrender"]:
        return 2


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


def insurance(dealerHand, playerHand): # Checks if the player wants to purchase insurance when dealer shows an Ace.
    insurance = False
    if dealerHand[1].value == 11 and isBJ(playerHand):
        insure = input("Would you like even money? y/n ")
        winType = "Even money"
        if yesNo(insure):
            insurance = True
        if isBJ(dealerHand):
            print("Dealer Blackjack!")
            if insurance:
                msgDivider(f"{winType} paid Out.")
            else:
                msgDivider(f"{winType} wasn't purchased, no payout.")
            printCards(dealerHand[0], False)
            printCards(dealerHand[1], False)
            if isBJ(playerHand):
                msgDivider("Blackjack! Push.")
            else:
                msgDivider("No blackjack, you lose.")
        else:
            msgDivider(f"No Blackjack! No {winType} payout.")
    elif dealerHand[1].value == 11 and not isBJ(playerHand):
        insure = input("Would you like to purchase insurance? y/n ")
        winType = "Insurance"
        if yesNo(insure):
            insurance = True
        if isBJ(dealerHand):
            msgDivider("Dealer Blackjack!")
            if insurance:
                msgDivider(f"{winType} Paid Out.")
            else:
                msgDivider(f"{winType} wasn't purchased, no payout.")
            printCards(dealerHand[0], False)
            printCards(dealerHand[1], False)
            if isBJ(playerHand):
                msgDivider("Blackjack! Push.")
            else:
                msgDivider("No blackjack, you lose.")
        else:
            msgDivider(f"No Blackjack! No {winType} payout.")


# Hit or stay function. Hidden surrender function inside.


def surrender(dealerHand, choice):
    if (not isBJ(dealerHand)) and choice:
        msgDivider("You surrendered your hand. Half your bet is returned.")
        return True
    return False


def hit(hand, deck, choice): # Deals a card, then returns card value if yes.
    if yesNo(choice):
        return dealCard(hand, deck)


def gameStart(deck):
    playerCards = []
    dealerCards = []
    playerValue = 0
    dealerValue = 0

    while len(playerCards) < 2: # Change to allow hits later (more than len of 2). Works for now due to testing.
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
            if not firstCard:
                print(f"Dealer Card: {card.value}")
            firstCard = False

        print(f"\nPlayer Total: {playerValue}\n")

        if len(dealerCards) == 2: # BJ Checker; Insurance y/n
            if (playerValue == 21 and dealerCards[1].value != 11) and (playerValue == 21 and dealerValue == 21):
                msgDivider("Dealer Blackjack; Push!")
                continue
            if (playerValue == 21 and dealerCards[1].value != 11) and (playerValue == 21 and dealerValue != 21):
                msgDivider("Blackjack!")
                continue
            insurance(dealerCards, playerCards)

            nextMove = nextPlay(input("Hit or stay? h/s "))
            if nextMove == 2:
                if surrender(dealerCards, True):
                    continue
            elif nextMove == 1:
                newCard = dealCard(playerCards, deck)
                playerValue += newCard
                print("Player Cards: ")
                for card in playerCards:
                    printCards(card, False)
                print(f"\nPlayer Total: {playerValue}\n")
                if playerValue > 21:
                    print("Bust!")
                    continue
            else:
                print("You stayed.")

    while len(playerCards) > 2 and playerValue < 21:
        firstCard = True
        print("Player Cards: ")
        for card in playerCards:
            printCards(card, False)

        print("Dealer Cards: ") # Dealer card printout. Slightly different since one card needs to be hidden.
        for card in dealerCards:
            printCards(card, firstCard)
            if not firstCard:
                print(f"Dealer Card: {card.value}")
            firstCard = False

        print(f"\nPlayer Total: {playerValue}\n")
        if playerValue > 21:
            print("Bust!")
            continue

        nextMove = nextPlay(input("Hit or stay? h/s "))
        if nextMove == 2:
            if surrender(dealerCards, True):
                continue
        elif nextMove == 1:
            newCard = dealCard(playerCards, deck)
            playerValue += newCard
        else:
            print("You stayed.")





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