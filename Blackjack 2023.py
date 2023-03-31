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
	print("_"*20, end=" ")
	print(msg, end=" ")
	print("_"*20)


def generateDeck(suits, suitValue, cards, cardValue):
	deck = []

	for suit in suits:
		for card in cards:
			deck.append(Card(suitValue[suit], card, cardValue[card]))

	return deck


def gameStart(deck):
	playerCards = []
	dealerCards = []
	playerValue = 0
	dealerValue = 0

	while len(playerCards) < 2:

		dealtCard = random.choice(deckOne)
		playerCards.append(dealtCard)
		deck.remove(dealtCard)

		playerValue += dealtCard.value

		print(f"Player Cards: ", end="")
		for card in playerCards:
			print(card.name, end=" ")
		print(f"\nTotal: {playerValue}")


msgDivider("Welcome to Toni's BJ Lounge")
deckOne = generateDeck(suits, suitValue, cards, cardValue)

gameStart(deckOne)