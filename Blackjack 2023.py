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


def generateDeck(suits, suitValue, cards, cardValue, size):
    deck = []
    for i in range(int(size)):
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
    yesOptions = ["y", "y.", "yes", "yes.", ""]
    noOptions = ["n", "n.", "no", "no.", "."]

    while choice.lower() not in yesOptions + noOptions:
        choice = input("Invalid input, try again: ")
    if choice.lower() in yesOptions:
        return True
    elif choice.lower() in noOptions:
        return False


def nextPlay(choice): # Returns a 0 if stay, 1 if hit, 2 if surrender, or 3 if double down.
    yesOptions = ["y", "y.", "yes", "yes.", ""]
    noOptions = ["n", "n.", "no", "no.", "."]
    surrOptions = ["surrender", "surr"]
    hitOptions = ["h", "hit"]
    ddOptions = ["d", "double", "dd"]
    stayOptions = ["s", "stay"]

    while choice.lower() not in yesOptions + noOptions + surrOptions + hitOptions + ddOptions + stayOptions:
        choice = input("Invalid input, try again: ")
    if choice.lower() in stayOptions + noOptions:
        return 0
    elif choice.lower() in yesOptions + hitOptions:
        return 1
    elif choice.lower() in surrOptions:
        return 2
    elif choice.lower() in ddOptions:
        return 3


def dealCard(hand, deck): # Deal card from deck, remove, returns dealt card value.
    dealtCard = random.choice(deck)
    hand.append(dealtCard)
    deck.remove(dealtCard)
    return dealtCard.value


def aces(hand, handTotal): # Prevents card total greater than 21 due to aces. Returns hand total.
    count = 0
    while handTotal > 21 and count < len(hand):
        if hand[count].value == 11:
            hand[count].value = 1
            handTotal -= 10
            count += 1
        else:
            count += 1
    return handTotal


def insurance(dealerHand, playerHand):# Checks if the player wants to purchase insurance when dealer shows an Ace.
    # Returns 0 if dealer BJ, otherwise 1.
    if dealerHand[1].value != 11:
        return 1

    isPlayerBJ = isBJ(playerHand)
    winType = "Even Money" if isPlayerBJ else "Insurance"
    question = f"Would you like {winType}? y/n "
    insurance = yesNo(input(question))

    if isBJ(dealerHand):
        print("Dealer Blackjack!")
        printCards(dealerHand[0], False)
        printCards(dealerHand[1], False)

        payoutMsg = f"{winType} paid out." if insurance else f"{winType} wasn't purchased, no payout."
        msgDivider(payoutMsg)

        if isPlayerBJ:
            msgDivider("Blackjack! Push.")
        else:
            msgDivider("No Blackjack, you lose.")
        return 0
    else:
        msgDivider(f"No Blackjack! No {winType} payout.")
        return 1


def surrender(dealerHand):
    if (not isBJ(dealerHand)):
        msgDivider("You surrendered your hand. Half your bet is returned.")
        return True
    return False


def doubleDown(playerHand, playerValue, deck):
    msgDivider("You doubled your bet.")
    newCard = dealCard(playerHand, deck)
    playerValue += newCard
    printCards(playerHand[len(playerHand) - 1], False)
    playerValue = aces(playerHand, playerValue)
    print(f"\nPlayer Total: {playerValue}\n")
    if playerValue > 21:
        print("Bust!")
    return True


def hit(hand, deck, choice): # Deals a card, then returns card value if yes.
    if yesNo(choice):
        return dealCard(hand, deck)


def playerHitLoop(playerHand, playerValue, dealerHand, dealerValue, deck):
    while len(playerHand) > 2 and playerValue < 21:
        print("Player Cards: ")
        for card in playerHand:
            printCards(card, False)

        print("Dealer Cards: ")
        for i in range(len(dealerHand)):
            if i == 0 and len(dealerHand) <= 2:
                printCards(dealerHand[i], True)
            else:
                printCards(dealerHand[i], False)
                print(f"Dealer Card: {dealerHand[i].value}")

        playerValue = aces(playerHand, playerValue)
        print(f"\nPlayer Total: {playerValue}\n")
        if playerValue > 21:
            msgDivider("Bust!")
            continue

        nextMove = nextPlay(input("Hit or stay? h/s "))
        while nextMove == 2 or nextMove == 3:
            nextMove = nextPlay(input("Invalid input, try again: h/s "))
        if nextMove == 1:
            newCard = dealCard(playerHand, deck)
            playerValue += newCard
            printCards(playerHand[len(playerHand) - 1], False)
            playerValue = aces(playerHand, playerValue)
            print(f"\nPlayer Total: {playerValue}\n")
            if playerValue > 21:
                print("Bust!")
                continue
        elif nextMove == 0:
            print("You stayed.")
            break # Need to add more to this. Aka Dealer draws.
        else: # Failsafe?
            print("You shouldn't reach this point.")


# Split Function. Separate the two cards into separate lists, or remove one into a new one. Act upon the two separately.



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
        dd = False

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
            if insurance(dealerCards, playerCards) == 0:
                continue

            if playerValue < 21:
                nextMove = nextPlay(input("Hit or stay? h/s "))
                if nextMove == 2:
                    if surrender(dealerCards):
                        continue
                elif nextMove == 1:
                    newCard = dealCard(playerCards, deck)
                    playerValue += newCard
                    printCards(playerCards[len(playerCards) - 1], False)
                    playerValue = aces(playerCards, playerValue)
                    print(f"\nPlayer Total: {playerValue}\n")
                    if playerValue > 21:
                        print("Player Cards: ")
                        for card in playerCards:
                            printCards(card, False)
                        print(f"\nPlayer Total: {playerValue}\n")
                        msgDivider("Bust!")
                        continue
                elif nextMove == 3:
                    dd = doubleDown(playerCards, playerValue, deck)
                elif nextMove == 0:
                    print("You stayed.") # Need to add more to this. Aka Dealer draws.
                else: # Failsafe?
                    print("You shouldn't reach this point.")

    if not dd:
        playerHitLoop(playerCards, playerValue, dealerCards, dealerValue, deck)
    #if dd and playerValue < 21: # Dealer draws.




#''' Swap between rigged and non rigged decks.

msgDivider("Welcome to Toni's BJ Lounge")
size = str(input("How many decks would you like to play? 1, 2, 6, or 8? "))
while size not in ["1", "2", "6", "8"]:
    size = str(input("Invalid input, try again: 1, 2, 6, or 8? "))
deck = generateDeck(suits, suitValue, cards, cardValue, size)
initialSize = len(deck)
run = True

while run:
    gameStart(deck)
    cont = input("Would you like to continue? y/n ")
    if not yesNo(cont):
        run = False
        break
    if int(size) != 1:
        if len(deck) <= initialSize * random.uniform(.1, .25): # Reshuffle randomly between 75%-90% remains.
            msgDivider("Reshuffled Deck")
            deck = generateDeck(suits, suitValue, cards, cardValue, size)
    else:
        if len(deck) <= initialSize * random.uniform(.2, .3):
            msgDivider("Reshuffled Deck")
            deck = generateDeck(suits, suitValue, cards, cardValue, size)

msgDivider("Thanks for playing!")


# _____ Rigged Deck ______ Used for testing :>
'''
#riggedCards = ["A", "10", "J", "K", "Q"]
riggedCards = ["A", "A", "A", "A"]
riggedCardValue = {"A":11, "10":10, "J":10, "K":10, "Q":10}

# _____ Rigged Deck _____
msgDivider("Rigged Deck Testing")
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

msgDivider("Thanks for playing!")
'''