import unittest
from Card import *
from Deck import *
from TriPeaks import*
from kapall import*

class Test(unittest.TestCase):

	def test_Card1(self):
		#make sure that cards are different
		t1 = Card('H',10, 0, 0, '')
		t2 = Card('H',11, 0, 0, '')
		self.assertNotEqual(t1,t2)

	def test_Card2(self):
		#Make sure that __eq__ that checks if cards are teh same, works
		t1 = Card('H',10, 0, 0, '')
		t2 = Card('H',11, 0, 0, '')
		t4 = t1.__eq__(t2)
		self.assertEqual(t4,False)

	def test_Card3(self):
		#same
		t1 = Card('H',11, 0, 0, '')
		t2 = Card('H',11, 0, 0, '')
		t4 = t1.__eq__(t2)
		self.assertEqual(t4,True)

		

	def test_shuffleCard(self):
		# make sure that shuffle does not loose cards
		self.seq = range(10)
		random.shuffle(self.seq)
		self.seq.sort()
		self.assertEqual(self.seq, range(10))
	
	def test_TriPeaks_decksize(self):
	#make sure that decksize is the same
		ta = TriPeaks()
		tb = TriPeaks()
		t1 = ta.deckSize()
		t2 = tb.deckSize()
		self.assertEqual(t1,t2)
		
	def test_TriPeaks2(self):
		# checks if initboard makes same size board each time
		t1 = TriPeaks()
		t2 = TriPeaks()
		tx = t1.initBoard()
		ty = t2.initBoard()
		self.assertEqual(tx, ty)
		
	
	def test_TriPeaks_Highscore(self):
		#checks if highscore works
		t1 = TriPeaks()
		x = t1.addScore(500)
		self.assertGreater(t1.score, 250)
		
	def test_TriPeaks_time(self):
		#checks if the time keeping works
		t1 = TriPeaks()
		time = t1.elapsedTime
		self.assertGreater(time, 0)
		
	def test_Moves(self):
		#makes sure moves is 0 at start
		t1 = TriPeaks()
		self.assertEqual(t1.moves,0) 	
		
	def test_isMovable(self):
		#checks if isMovable works, that is if a card is Movable from 'pyramid'
		t1 = TriPeaks()
		t2 = t1.isMovable(3,3)
		self.assertEqual(t2,True)
		

		

		
if __name__== '__main__':
  unittest.main()
