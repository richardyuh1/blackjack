import random 
from time import sleep 

# Card ranks 
RANK = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}

# Card suits: Club, Diamond, Heart, Spade
SUIT = {'C': 1, 'D': 2, 'H': 3, 'S': 4}

class Card: 
	
	def __init__(self, rank, suit):
		self.rank = rank 
		self.suit = suit 

	def __repr__(self): 
		return "{}{}".format(self.rank, self.suit)

	def __str__(self): 
		return "{}{}".format(self.rank, self.suit)

	def suit_value(self): 
		return SUIT[self.suit]

	def rank_value(self): 
		if self.rank.isdigit(): 
			return int(self.rank)
		if self.rank == 'J': 
			return 11  
		if self.rank == 'Q': 
			return 12 
		if self.rank == 'K': 
			return 13 
		if self.rank == 'A': 
			return 14 

class Deck:

	def __init__(self): 
		self.cards = [] 
		self.build()

	def __len__(self): 
		return len(self.cards)

	def build(self): 
		self.cards = [Card(rank, suit) for suit in SUIT for rank in RANK]

	def draw(self): 
		if len(self.cards) <= 0: 
			print('Deck is empty, can no longer draw')
			return 
		return self.cards.pop() 

	def shuffle(self):
		for i in range(len(self.cards)): 
			rand_int = random.randint(0, len(self.cards)-1)
			self.cards[i], self.cards[rand_int] = self.cards[rand_int], self.cards[i]

	def sort(self): 
		self.cards.sort(key=lambda x: (x.suit_value(), x.rank_value()))

	def show(self): 
		print(deck.cards)

class Player: 
	def __init__(self, deck, name): 
		self.hand = []
		self.deck = deck
		self.name = name 

	def __repr__(self): 
		return "Player Name: {}, Hand: {}".format(self.name, self.hand)

	def __str__(self): 
		return "Player Name: {}, Hand: {}".format(self.name, self.hand)

	def draw(self, n): 
		for _ in range(n): 
			card = self.deck.draw() 
			if card: 
				self.hand.append(card) 
			else: 
				print('No card to draw for player')

	def deal(self): 
		self.draw(2) 

	def score(self): 
		score_ace_low, score_ace_high = 0, 0
		for card in self.hand: 
			if card.rank in {'J', 'Q', 'K'}:
				score_ace_low += 10 
				score_ace_high += 10 
			elif card.rank == 'A': 
				score_ace_low += 1 
				score_ace_high += 10 
			else: 
				score_ace_low += card.rank_value() 
				score_ace_high += card.rank_value()
		return (score_ace_low, score_ace_high)  

	def final_score(self): 
		score = self.score() 
		if score[0] == score[1]: 
			return score[0] 
		if score[0] > 21 and score[1] > 21: 
			return min(score[0], score[1])
		if score[0] > 21: 
			return score[1] 
		if score[1] > 21: 
			return score[0] 
		return max(score[0], score[1])

	def bust(self): 
		return min(self.score()) > 21

	def show(self): 
		score = self.score() 
		if score[0] == score[1] or score[1] > 21: 
			score = score[0] 
		else: 
			score = "{},{}".format(score[0], score[1])
		print("{}'s hand: {}, score: {}".format(self.name, self.hand, score))

class Blackjack: 
	def __init__(self, deck): 
		self.deck = deck 

	def play(self): 
		print("Welcome to Blackjack.")
		dealer = Player(self.deck, "Dealer") 
		player_name = input("Enter name of player: ")
		player = Player(self.deck, player_name)
		dealer.deal() 
		player.deal() 
		dealer.show() 
		player.show()
		
		player_stand = False 
		while not player_stand: 
			print('=========================================')
			player.show()
			shouldHit = input("{}'s turn. Hit or stand (H or S): ".format(player.name))
			while shouldHit != 'H' and shouldHit != 'S': 
				shouldHit = input("Try again. {}'s turn. Hit or stand (H or S): ".format(player.name))
			if shouldHit == 'H': 
				player.draw(1) 
				if player.bust():
					player.show()
					print('=========================================')
					print("{} wins. {} loses".format(dealer.name, player.name))
					return 
				if player.score()[0] == 21 or player.score()[1] == 21: 
					player.show()
					print('=========================================')
					print("{} wins. {} loses".format(player.name, dealer.name))
					return 
			else: 
				player_stand = True 
		
		dealer_stand = False 
		while not dealer_stand: 
			print('=========================================')
			dealer.show()
			shouldHit = input("{}'s turn. Hit or stand (H or S): ".format(dealer.name))
			while shouldHit != 'H' and shouldHit != 'S': 
				shouldHit = input("Try again. {}'s turn. Hit or stand (H or S): ".format(dealer.name))
			if shouldHit == 'H': 
				dealer.draw(1) 
				if dealer.bust(): 
					dealer.show()
					print('=========================================')
					print("{} wins. {} loses".format(player.name, dealer.name))
					return 
				if dealer.score()[0] == 21 or dealer.score()[1] == 21: 
					dealer.show()
					print('=========================================')
					print("{} wins. {} loses".format(dealer.name, player.name))
					return
			else: 
				dealer_stand = True 

		dealer_score = dealer.final_score() 
		player_score = player.final_score()
		print('=========================================')
		if dealer_score > player_score: 
			print("{} wins. {} loses. Final score: {} - {}".format(dealer.name, player.name, dealer_score, player_score))
		if dealer_score == player_score: 
			print("Tie game. Final score: {} - {}".format(dealer.name, player.name, dealer_score, player_score))
		else: 
			print("{} wins. {} loses. Final score: {} - {}".format(player.name, dealer.name, player_score, dealer_score))

if __name__ == '__main__':
	deck = Deck() 
	deck.shuffle() 
	b = Blackjack(deck)
	b.play()

