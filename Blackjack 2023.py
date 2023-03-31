import random


class Card:
	def __init__(self, suit, name, value):
		self.suit = suit
		self.name = name # Name of card, i.e. Ace, King, Queen, etc.
		self.value = value # Numerical value.


suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
suitValue = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs":"\u2667", "Diamonds":"\u2662"}
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "10", "J", "K", "Q"]
cardValue = {"A":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "K":10, "Q":10}


def msgDivider(msg):
	print("_" * 20, end=" ")
	print(msg, end=" ")
	print("_" * 20)


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
	while choice.lower() not in ["y", "y.", "yes", "yes.", "n", "n.", "no", "no."]:
		choice = input("Invalid input, try again: ")
	if choice.lower() in ["y", "y." "yes", "yes."]:
		return True
	elif choice.lower() in ["n", "n." "no", "no."]:
		return False


def gameStart(deck):
	playerCards = []
	dealerCards = []
	playerValue = 0
	dealerValue = 0
	insurance = False

	while len(playerCards) < 2:

		dealtCard = random.choice(deck)
		playerCards.append(dealtCard)
		deck.remove(dealtCard)
		playerValue += dealtCard.value

		firstCard = True
		dealtCard = random.choice(deck)
		dealerCards.append(dealtCard)
		dealerValue += dealtCard.value

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

		if len(dealerCards) == 2: # BJ checker; Insurance y/n
			if dealerCards[1].value == 10 or dealerCards[1].value == 11:
				insure = input("Would you like to purchase insurance? y/n ")
				if yesNo(insure):
					insurance = True
				if isBJ(dealerCards):
					print("Dealer Blackjack! Insurance Paid Out.")
					printCards(dealerCards[0], False)
					printCards(dealerCards[1], False)
				else:
					print("No Blackjack! No Pay Out.")





msgDivider("Welcome to Toni's BJ Lounge")
deckOne = generateDeck(suits, suitValue, cards, cardValue)

gameStart(deckOne)