import os, pygame,math
from pygame.locals import *
                             
class Card:

    def __init__(self,frontImage,backImage,x=0,y=0):
        self.bimg = backImage
        self.fimg = frontImage
        self.img = backImage
        self.side = 0
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.child = None
        self.parent = None
        self.selected = 0

    def flip(self):
        if self.side==1:
            self.side = 0
            self.img = self.bimg
        else:
            self.side = 1
            self.img = self.fimg

    def backSide(self):
        self.side = 0
        self.img = self.bimg

    def frontSide(self):
        self.side = 1
        self.img = self.fimg

    def setSide(self,side):
        if side:
            self.img = self.fimg
        else:
            self.img = self.bimg
        self.side = side
       
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
        if self.child:
            self.child.move(dx,dy)

    def draw(self,surface):
        surface.blit(self.img,self.rect.topleft)
