# Class for a card in a deck
class Card(object):
    
    # Creates a new card with a sort and a value
    def __init__(self, sort, value, x, y, img):
        self.sort = sort
        self.value = value
        self.cardx = x
        self.cardy = y
        self.img = img
        
    # Called when a card object is printed
    def __repr__(self):
        return self.toString()
    
    # Comparator for card objects
    def __eq__(self,other):
        return (self.sort == other.sort and self.value == other.value)


    def toString(self):
        return str(self.sort) + str(self.value)
