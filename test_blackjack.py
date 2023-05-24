import unittest
import Blackjack_2023 as bj

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
		deck = bj.generate_deck(suits, suit_value, cards, card_value, 1)
		self.assertEqual(52, len(deck))
		deck = bj.generate_deck(suits, suit_value, cards, card_value, 2)
		self.assertEqual(104, len(deck))
		deck = bj.generate_deck(suits, suit_value, cards, card_value, 6)
		self.assertEqual(312, len(deck))
		deck = bj.generate_deck(suits, suit_value, cards, card_value, 8)
		self.assertEqual(416, len(deck))

	def test_blackjack(self):
		hand = [bj.Card("\u2662", "K", 10), bj.Card("\u2664", "A", 11)]
		self.assertEqual(True, bj.Hand(hand).is_blackjack())
		hand = [bj.Card("u2662", "A", 11), bj.Card("u2664", "Q", 10)]
		self.assertEqual(True, bj.Hand(hand).is_blackjack())
		hand = [bj.Card("\u2662", "K", 10), bj.Card("\u2664", "Q", 10)]
		self.assertEqual(False, bj.Hand(hand).is_blackjack())

	def test_deal_card(self):
		deck = [bj.Card("\u2662", "K", 10), bj.Card("\u2664", "A", 11), bj.Card("\u2661", "9", 9),
		bj.Card("\u2667", "8", 8)]
		hand = []
		self.assertEqual(4, len(deck))
		self.assertEqual(0, len(bj.Hand(hand).cards))
		bj.Hand(hand).deal_card(deck)
		self.assertEqual(3, len(deck))
		self.assertEqual(1, len(bj.Hand(hand).cards))
		self.assertEqual(False, bj.Hand(hand).cards[0] in deck)

	def test_hand_value(self):
		hand = [bj.Card("\u2662", "K", 10), bj.Card("\u2664", "A", 11)]
		value = bj.Hand(hand).get_hand_value()
		self.assertEqual(21, value)
		hand = [bj.Card("\u2662", "7", 7), bj.Card("\u2664", "3", 3)]
		value = bj.Hand(hand).get_hand_value()
		self.assertEqual(10, value)
		# Testing for aces.
		hand = [bj.Card("\u2662", "A", 11), bj.Card("\u2664", "A", 11)]
		value = bj.Hand(hand).get_hand_value()
		self.assertEqual(12, value)
		hand = [bj.Card("\u2662", "A", 11), bj.Card("\u2664", "J", 10), bj.Card("\u2661", "9", 9)]
		value = bj.Hand(hand).get_hand_value()
		self.assertEqual(20, value)
		hand = [bj.Card("\u2662", "A", 11), bj.Card("\u2664", "J", 10), bj.Card("\u2661", "9", 9),
		bj.Card("\u2662", "A", 11)]
		value = bj.Hand(hand).get_hand_value()
		self.assertEqual(21, value)
	'''
	def test_dd(self):
		hand = [bj.Card("\u2662", "5", 5), bj.Card("\u2664", "5", 5)]
		deck = [bj.Card("\u2662", "2", 2)]
		bj.double_down(hand, bj.get_hand_value(hand), deck)
		self.assertEqual(12, bj.get_hand_value(hand))
		hand = [bj.Card("\u2662", "10", 10), bj.Card("\u2664", "10", 10)]
		deck = [bj.Card("\u2662", "2", 2)]
		bj.double_down(hand, bj.get_hand_value(hand), deck)
		self.assertEqual(22, bj.get_hand_value(hand))
	'''

if __name__ == '__main__':
    unittest.main()