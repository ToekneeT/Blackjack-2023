import unittest
#import Blackjack_2023
from Blackjack_2023 import Card, generate_deck, is_blackjack

class BlackjackTest(unittest.TestCase):
	def test_deck_size(self):
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
		deck = generate_deck(suits, suit_value, cards, card_value, 1)
		self.assertEqual(52, len(deck))
		deck = generate_deck(suits, suit_value, cards, card_value, 2)
		self.assertEqual(104, len(deck))
		deck = generate_deck(suits, suit_value, cards, card_value, 6)
		self.assertEqual(312, len(deck))
		deck = generate_deck(suits, suit_value, cards, card_value, 8)
		self.assertEqual(416, len(deck))

	def test_blackjack(self):
		hand = [Card("Diamonds", "\u2662", 10), Card("Spades", "\u2664", 11)]
		self.assertEqual(True, is_blackjack(hand))
		hand = [Card("Diamonds", "\u2662", 11), Card("Spades", "\u2664", 10)]
		self.assertEqual(True, is_blackjack(hand))
		hand = [Card("Diamonds", "\u2662", 10), Card("Spades", "\u2664", 10)]
		self.assertEqual(False, is_blackjack(hand))


if __name__ == '__main__':
    unittest.main()