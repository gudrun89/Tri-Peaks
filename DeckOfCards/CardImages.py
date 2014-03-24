
import os, pygame,math
from pygame.locals import *
                             
class CardImages:

    S = 0
    C = 1
    D = 2
    H = 3
    
    cardImages = []
    backImage = None

    def __init__(self):
    
        colors = ['s','c','d','h']
        values = ['a','2','3','4','5','6','7','8','9','t','j','q','k']

        for c in colors:
            for v in values:
                self.cardImages.append(pygame.image.load("./cards/%s%s.gif" % (v,c)).convert())

        self.backImage = pygame.image.load("./cards/b.gif")

        #colors = ['spade','club','diamond','heart']
        #values = ['1','2','3','4','5','6','7','8','9','10','jack','queen','king']

        #for c in colors:
        #    for v in values:
        #        self.cardImages.append(pygame.image.load("./CardPng/%s_%s.png" % (v,c)))

        #self.backImage = pygame.image.load("./CardPng/back.png")


    def getCard(self,color,value):
        return self.cardImages[(color*13)+(value-1)]

    def getCardNbr(self,nbr):
        return self.cardImages[nbr]

    def getBack(self):
        return self.backImage
    

