import random
from Card import *

# Class for a deck of cards
class Deck(object):
    
    # Creates a new deck with 'noCards' number of cards
    def __init__(self, numCards, cards=None):
        self.cards = []
        self.setCards(numCards)

    # Called when a Deck object is printed
    def __repr__(self):
        return str(self.cards)

        
    # Pre:  cards is a list of Card objects
    # Post: all Card objects in cards have been added to Deck.cards,
    #       if no list of Card objects is indicated, then a normal 52
    #       deck is initialized
    # Run:  Deck.setCards() or Deck.setCards(cards)
    def setCards(self, numCards, cards=None):
        ''' Initializes the cards in the deck '''
        if cards is None:
            self.cards = []
            col = 0
            row = 0
            for i in range(1,(numCards/4 + 1)):
                for sort in ['H', 'S', 'T', 'L']:
                    self.cards.append(Card(sort,i, col, row, "./cards/%s%s.gif" % (i,sort.lower())))
        else:
            self.cards = cards
    
    def shuffleCards(self):
        ''' Shuffles the order of the cards in the deck '''
        random.shuffle(self.cards)

    def isEmpty(self):
        ''' Checks if the deck is empty '''
        return len(self.cards) == 0
    
    def getCard(self,i):
        ''' Returns card number 'i' in the deck '''
        return self.cards[i]
    
    def getNextCard(self):
        ''' Returns the next card in the deck '''
        if (not self.isEmpty()):
            return self.cards[0]
    
    def addCard(self, card):
        ''' Adds the card 'card' to the deck '''
        self.cards.append(card)
        
    
    def removeCard(self, card):
        ''' Removes the card 'card' from the deck '''
        if (not self.isEmpty()):
            self.cards.remove(card)        
