# Class for a card in a deck
class Card(object):
    
    # Creates a new card with a sort and a value
    def __init__(self, sort, value, col, row, img):
        self.sort = sort
        self.value = value
        self.col = col
        self.row = row
        self.img = img
        self.cardx = 0
        self.cardy = 0
        
    # Called when a card object is printed
    def __repr__(self):
        return self.toString()
    
    # Comparator for card objects
    def __eq__(self,other):
        return (self.sort == other.sort and self.value == other.value)

    def toString(self):
        return str(self.sort) + str(self.value)

    def moveTo(self,x,y):
        self.cardx = x
        self.cardy = y
