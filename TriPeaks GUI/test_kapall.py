import unittest
from Card import *
from Deck import *
from TriPeaks import*
from kapall import*

class Test(unittest.TestCase):

    def setUp(self):
        self.testCard1a = Card('H',10, 0, 0, None)
        self.testCard1b = Card('H',10, 0, 0, None)
        self.testCard2a = Card('S',5, 0, 0, None)
        self.testCard2b = Card('S',5, 0, 0, None)
        self.testCard3 = Card('T',3, 0, 0, None)
        self.initialDeck = Deck(52)
        self.sortedDeck = Deck(52)
        self.sortedDeck.cards.sort()
        self.shuffledDeck = Deck(52)
        self.shuffledDeck.shuffleCards()
        self.game1 = TriPeaks()
        self.game2 = TriPeaks()
        self.deckCard = self.game1.deck.cards[-1]
        self.heapCard = self.game1.heap[-1]
        self.legalCard = Card('H', (self.heapCard.value)%13+1, 3,3,None)
        self.illegalCard = Card('H', (self.heapCard.value)%13+5, 0,0,None)

    def test_Card1(self):
        #make sure that the cards are different
        self.assertNotEqual(self.testCard2a,self.testCard3)

    def test_Card2(self):
        #make sure that that the cards are equal
        self.assertEqual(self.testCard1a,self.testCard1b)

    def test_Card3(self):
        #make sure that that the cards are equal
        self.assertEqual(self.testCard2a,self.testCard2b)

    def test_shuffleCards(self):
        # make sure that shuffle maintains the same cards
        self.shuffledDeck.cards.sort()
        self.assertTrue(self.shuffledDeck.cards == self.sortedDeck.cards)
    
    def test_deckSize(self):
        #make sure that decksize is the same
        self.assertEqual(self.game1.deckSize(),self.game2.deckSize())
        
    def test_initBoard(self):
        #make sure that initboard makes same size board each time
        self.assertEqual(self.game1.initBoard(), self.game2.initBoard())
        
    def test_addScore(self):
        #make sure that addScore adds to the score
        self.game1.addScore(500)
        self.assertEqual(self.game1.score, 500)
        
    def test_Moves(self):
        #makes sure that moves starts at 0
        self.assertEqual(self.game1.moves,0)
        
    def test_isMovable1(self):
        #make sure that card is movable
        self.assertTrue(self.game1.isMovable(3,3))

    def test_isMovable2(self):
        #make sure that card is not movable
        self.assertFalse(self.game1.isMovable(1,1))

    def test_isLegal1(self):
        # make sure that card is legal
        self.assertTrue(self.game1.isLegal(self.legalCard))

    def test_isLegal2(self):
        # make sure that card is illegal
        self.assertFalse(self.game1.isLegal(self.illegalCard))

    def test_moveToHeap(self):
        # make sure that card is added to heap
        movedCard = self.game1.moveToHeap(self.legalCard)
        self.assertEqual(movedCard, self.legalCard)
        self.assertIn(self.legalCard, self.game1.heap)
        

    def test_toHeap(self):
        # make sure that card is removed from deck and added to heap
        self.game1.toHeap()
        self.assertIn(self.deckCard, self.game1.heap)
        self.assertNotIn(self.deckCard, self.game1.deck.cards)
        

        
if __name__== '__main__':
  unittest.main()
