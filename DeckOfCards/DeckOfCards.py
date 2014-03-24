
#/usr/bin/env python

import os, pygame,math
from pygame.locals import *
import random

from CardImages import CardImages
from CardGroup import CardGroup
from Card import Card
                             
class DeckOfCards:


    def initKlondike(self):
        self.mode = self.NOTHING        
        cg = self.cardGroup
        self.selectionRect = pygame.Rect((0,0,0,0))
        self.selectionCards = []  
        cg.collectAll(15,15)
        cg.shuffle()
          
        gt = cg.getCardAt  
                
        cards = 0
        x = 10
        y = 140
        idx = 51
        
        for cols in range(7):
            for hc in range(cards):
                c = gt(idx)
                idx-=1
                c.rect.x = x
                c.rect.y = y
                cg.dropCard(c)
                y+=20
            c = gt(idx)
            idx-=1
            c.flip()
            c.rect.x = x
            c.rect.y = y
            cg.dropCard(c)
            cards+=1
            x+=90
            y=140
  
    NOTHING = 0
    DRAW_SELECTION = 1
    CARD_SELECTED = 2
    SELECTION_SELECTED = 3
    SELECTION_SPREAD_INIT = 4
    SELECTION_SPREAD = 5

    MAX_HISTORY = 30
    history = []
    
    def clearHistory(self):
        self.history = []

    def pushHistory(self,desc):
        #print "Pushing: %s" % desc
        while len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)
        
        # store get the z-order
        cards = self.cardGroup.cards[:]
        
        # store card info
        cardinfo = []
        for c in cards:
            info = []
            info.append(c.side)
            info.append(c.rect.topleft)
            info.append(c.child)
            info.append(c.parent)
            info.append(c.selected)
            cardinfo.append(info)
        
        if len(self.selectionCards):
            selrect = pygame.Rect(self.selectionRect)
            selcards = self.selectionCards[:]
        else:
            selrect = pygame.Rect((0,0,0,0))
            selcards = []  
       
        self.history.append([cards,cardinfo,selrect,selcards,desc])
 
    def popHistory(self):
        if not len(self.history):
            return
    
        hi = self.history.pop()
        
        #print "Popping: %s" % hi[4]
        
        cards = hi[0]
        
        i = 0
        for ci in hi[1]:
            cards[i].setSide(ci[0])
            cards[i].rect.topleft = ci[1]
            cards[i].child = ci[2]
            cards[i].parent = ci[3]
            cards[i].selected = ci[4]            
            i+=1
            
        self.cardGroup.cards = cards   
        self.selectionRect = hi[2]   
        self.selectionCards = hi[3]        
                   
    def updateSelectionRect(self):
        r = None
        for c in self.selectionCards:
            if not r:
                r = pygame.Rect(c.rect)
            else:
                r.union_ip(c.rect)        
        r.x-=3
        r.y-=3
        r.width+=6
        r.height+=6
                
        self.selectionRect = r

    def shuffleSelection(self):
        if len(self.selectionCards):
            rectbuf = []
            for c in self.selectionCards:
                rectbuf.append(pygame.Rect(c.rect))

            random.shuffle(self.selectionCards)                    

            for i in range(len(rectbuf)):
                self.selectionCards[i].rect = rectbuf[i]

            self.cardGroup.popCards(self.selectionCards)                            
        
 
    text = [
        "DeckOfCards v1.0",
        "-----------------------",
        "F1 - Display this help text.",
        "F2 - Collect cards and shuffle deck.",
        "F3 - Setup for Klondike solitaire.",
        "Arrow keys - Align selected cards.",
        "Left mouse - Move or select cards.",
        "Right mouse - Flip single or selected.",
        "Middle mouse - Pick single card.",
        "Mouse click + shift - Collect selected cards.",
        "Mouse drag + shift - Layout selected cards.",
        "Ctrl+T - Toggle sticky cards.",
        "Ctrl+S - Shuffle selected cards.",
	"Ctrl+Z - Undo latest action.",
        "-----------------------",
        "press any key to continue"]
        

    def mainLoop(self):    
        pygame.init()    

        self.screen = pygame.display.set_mode((640, 480),HWSURFACE|RESIZABLE)
        pygame.display.set_caption('DeckOfCards - v1.0')
                              
        self.selectedCard = None
    
        self.selectionRect = pygame.Rect((0,0,0,0))
        self.selectionCards = []  
               
        ci = CardImages()
 
        cards = []
        for i in range(0,52):
            cards.append(Card(ci.getCardNbr(i),ci.getBack(),30,30))

	#second deck
        #for i in range(0,52):
        #    cards.append(Card(ci.getCardNbr(i),ci.getBack(),15,15))
                   
        self.cardGroup = CardGroup(cards)
        self.cardGroup.shuffle()        
                
        self.mode = self.NOTHING        
                        
        popsingle = 0

        self.helptext = pygame.Surface((380,420),1).convert()
        self.helptext.fill((0x0, 0x0, 0x0))
        self.helptext.set_alpha(200);
        self.helptextRect = self.helptext.get_rect()
                
        font = pygame.font.Font("FreeSans.ttf", 18)
        ty = 8
        for t in self.text:
          img = font.render(t, 1, (0xff, 0xff, 0))
          r = img.get_rect()
          r.top = ty
          r.centerx = self.helptextRect.centerx
          ty += 25
          self.helptext.blit(img,r.topleft)
        
        viewhelp = 1
        sr = self.screen.get_rect()
        self.helptextRect.centerx = sr.centerx
        self.helptextRect.centery = sr.centery
                         
        lctrlDown = 0
        rctrlDown = 0
        lshiftDown = 0
        rshiftDown = 0
                                            
        while 1:                                                                      
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size,HWSURFACE|RESIZABLE)
                    if viewhelp:
                        sr = self.screen.get_rect()
                        self.helptextRect.centerx = sr.centerx
                        self.helptextRect.centery = sr.centery
                elif event.type == KEYDOWN:          
                    #print "key = %s" % str(event.key)
                    #print "keyname = %s" % pygame.key.name(event.key)
                    if viewhelp:
                        if event.key == K_ESCAPE:
                            return                    
                        viewhelp=0
                        continue                                                  
                    if event.key == K_ESCAPE:
                        return                    
                    elif event.key == K_LCTRL:
                        lctrlDown = 1        
                    elif event.key == K_RCTRL:
                        rctrlDown = 1        
                    elif event.key == K_LSHIFT:
                        lshiftDown = 1        
                    elif event.key == K_RSHIFT:
                        rshiftDown = 1        
                    elif event.key == 122 and (lctrlDown or rctrlDown):                        
                            self.popHistory()
                    elif event.key == 116 and (lctrlDown or rctrlDown):                        
                        if popsingle:
                            popsingle = 0
                        else:
                            popsingle = 1
                    elif event.key == 115 and (lctrlDown or rctrlDown):                        
                        self.pushHistory("Selection shuffle")
                        self.shuffleSelection()
                    elif event.key == K_F1:
                        if self.mode == self.NOTHING:
                            sr = self.screen.get_rect()
                            self.helptextRect.centerx = sr.centerx
                            self.helptextRect.centery = sr.centery                            
                            viewhelp = 1
                    elif event.key == K_F2:
                        self.pushHistory("F2")
                        self.selectionRect = pygame.Rect((0,0,0,0))
                        self.selectionCards = []  
                        self.cardGroup.collectAll(30,30)
                        self.cardGroup.shuffle()
                    elif event.key == K_F3:
                        self.pushHistory("Setup Klondike")
                        self.initKlondike()
                    elif event.key == K_LEFT:
                        if len(self.selectionCards):
                            self.pushHistory("AlignLeft")
                            left = self.selectionCards[0].rect.left
                            for c in self.selectionCards:
                                if c.rect.left<left:
                                    left = c.rect.left
                            for c in self.selectionCards:
                                c.rect.left = left
                            self.updateSelectionRect()
                    elif event.key == K_RIGHT:
                        if len(self.selectionCards):
                            self.pushHistory("AlignRight")
                            right = self.selectionCards[0].rect.right
                            for c in self.selectionCards:
                                if c.rect.right>right:
                                    right = c.rect.right
                            for c in self.selectionCards:
                                c.rect.right = right
                            self.updateSelectionRect()
                    elif event.key == K_UP:
                        if len(self.selectionCards):
                            self.pushHistory("AlignUp")
                            top = self.selectionCards[0].rect.top
                            for c in self.selectionCards:
                                if c.rect.top<top:
                                    top = c.rect.top
                            for c in self.selectionCards:
                                    c.rect.top = top
                            self.updateSelectionRect()
                    elif event.key == K_DOWN:
                        if len(self.selectionCards):
                            self.pushHistory("AlignDown")
                            bottom = self.selectionCards[0].rect.bottom
                            for c in self.selectionCards:
                                if c.rect.bottom>bottom:
                                    bottom = c.rect.bottom
                            for c in self.selectionCards:
                                c.rect.bottom = bottom
                            self.updateSelectionRect()
                elif event.type == KEYUP:          
                    if event.key == K_LCTRL:
                        lctrlDown = 0        
                    elif event.key == K_RCTRL:
                        rctrlDown = 0        
                    elif event.key == K_LSHIFT:
                        lshiftDown = 0        
                    elif event.key == K_RSHIFT:
                        rshiftDown = 0        
                        
                elif event.type == MOUSEBUTTONDOWN and viewhelp == 0:
                    if self.mode == self.NOTHING and (event.button in [1,2,3]):                        
                        #Check if we are inside selection.
                        if self.selectionRect.width > 0 and self.selectionRect.height > 0:
                            if self.selectionRect.collidepoint(event.pos[0],event.pos[1]):
                                if lshiftDown or rshiftDown:
                                
                                    if len(self.selectionCards) >= 2:
                                        self.pushHistory("Collecting/spreading selection")

                                        cx = self.selectionCards[0].rect.centerx
                                        cy = self.selectionCards[0].rect.centery
                                        for c in self.selectionCards:
                                            c.rect.centerx = cx
                                            c.rect.centery = cy
                                        self.updateSelectionRect()

                                        if event.button == 3:
                                            self.selectionCards.reverse()
                                            for c in self.selectionCards:
                                                c.flip()
                                        self.cardGroup.popCards(self.selectionCards)
                                    
                                        pygame.mouse.set_pos((cx,cy))
                                        self.mode = self.SELECTION_SPREAD_INIT
                                else:
                                    self.pushHistory("Pop/flip selection")
                                    self.mode = self.SELECTION_SELECTED
                                    if event.button == 3:
                                        self.selectionCards.reverse()
                                        for c in self.selectionCards:
                                            c.flip()
                                    self.cardGroup.popCards(self.selectionCards)                            

                        if self.mode == self.NOTHING:                            
                            if len(self.selectionCards):
                                self.pushHistory("Drop selection cards")
                                self.cardGroup.popCards(self.selectionCards)                            
                                self.cardGroup.dropCards(self.selectionCards)
                                self.selectionCards = []
                                self.selectionRect.size=(0,0)
                        
                        #Check if any card is selected.
                        if self.mode == self.NOTHING:                            
                            pop = popsingle
                            if event.button == 2:
                            	popsingle = 1
                            self.pushHistory("Pop/flip selected card")
                            self.selectedCard = self.cardGroup.getCard(event.pos[0],event.pos[1],popsingle)                        
                            if event.button == 2:
                            	popsingle = pop
                            if self.selectedCard:                                                               
                                self.mode = self.CARD_SELECTED
                                if event.button == 3:
                                    self.selectedCard.flip()                    
                            else:
                                self.history.pop()
                        #Init a new selection rectangle.
                        if self.mode == self.NOTHING:                                 
                            self.selectionStart = (event.pos[0],event.pos[1])
                            self.mode = self.DRAW_SELECTION
                                                        
                elif event.type == MOUSEBUTTONUP and viewhelp == 0:
                
                        if self.mode == self.SELECTION_SELECTED:
                            self.mode = self.NOTHING

                        elif self.mode == self.SELECTION_SPREAD:
                            self.mode = self.NOTHING

                        elif self.mode == self.SELECTION_SPREAD_INIT:
                            self.mode = self.NOTHING
                
                        elif self.mode == self.CARD_SELECTED:
                            #self.pushHistory("Drop card")
                            self.cardGroup.dropCard(self.selectedCard)
                            self.selectedCard = None 
                            self.mode = self.NOTHING
                            
                        elif self.mode == self.DRAW_SELECTION:
                            #see if we have selected any cards
                            if self.selectionRect.width > 0 and self.selectionRect.height > 0:
                                self.pushHistory("Select cards")
                                self.selectionRect,self.selectionCards = self.cardGroup.getCards(self.selectionRect)
                                if not len(self.selectionCards):
                                    self.history.pop()
                            self.mode = self.NOTHING
                            
                elif event.type == MOUSEMOTION and viewhelp == 0:
                    if event.buttons[0] or event.buttons[1] or event.buttons[2]:
                        if self.mode == self.SELECTION_SELECTED:
                            #Handle the drag of a selection rectangle.
                            if len(self.selectionCards):
                                self.selectionRect.topleft = (self.selectionRect.x+event.rel[0],self.selectionRect.y+event.rel[1])
                                for c in self.selectionCards:
                                    c.move(event.rel[0],event.rel[1]);

                        elif self.mode == self.SELECTION_SPREAD_INIT:
                            self.mode = self.SELECTION_SPREAD

                        elif self.mode == self.SELECTION_SPREAD:
                            #Handle the spread of a selection rectangle.
                            l = len(self.selectionCards)
                            if l>=2:          
                            
                                c = self.selectionCards[l-1]
                                fc = self.selectionCards[0]
                            
                                dx = event.pos[0]-fc.rect.centerx
                                dy = event.pos[1]-fc.rect.centery                                                      
                                
                                if abs(dx) > abs(dy):
                                    cnt = 0                       
                                    d = float(dx)/float(l-1)
                                    for mc in self.selectionCards:
                                        mc.rect.centery = fc.rect.centery
                                        mc.rect.centerx = fc.rect.centerx+int(d*cnt)
                                        cnt += 1
                                    c.rect.centerx = event.pos[0]
                                    c.rect.centery = fc.rect.centery
                                else:
                                    cnt = 0 
                                    d = float(dy)/float(l-1)
                                    for mc in self.selectionCards:
                                        mc.rect.centerx = fc.rect.centerx
                                        mc.rect.centery = fc.rect.centery+int(d*cnt)
                                        cnt += 1
                                    c.rect.centery = event.pos[1]
                                    c.rect.centerx = fc.rect.centerx

                                r = pygame.Rect(c.rect)
                                r.union_ip(self.selectionCards[0].rect)        
                                r.x-=3
                                r.y-=3
                                r.width+=6
                                r.height+=6
                                self.selectionRect = r
                  
                        elif self.mode == self.CARD_SELECTED:
                            #Handle the drag of a selected card.
                            self.selectedCard.move(event.rel[0],event.rel[1]);
                        
                        elif self.mode == self.DRAW_SELECTION: 
                            #Handle the selection rectangle
                            #self.selectionRect.size=(event.pos[0]-self.selectionRect.x,event.pos[1]-self.selectionRect.y)

                            if event.pos[0] <= self.selectionStart[0]:
                                self.selectionRect.x = self.selectionStart[0]-(self.selectionStart[0]-event.pos[0])
                                self.selectionRect.width = self.selectionStart[0]-event.pos[0]
                            else:                            
                                self.selectionRect.x=self.selectionStart[0]
                                self.selectionRect.width=event.pos[0]-self.selectionStart[0]

                            if event.pos[1] <= self.selectionStart[1]:
                                self.selectionRect.y = self.selectionStart[1]-(self.selectionStart[1]-event.pos[1])
                                self.selectionRect.height = self.selectionStart[1]-event.pos[1]
                            else:                            
                                self.selectionRect.y=self.selectionStart[1]
                                self.selectionRect.height=event.pos[1]-self.selectionStart[1]
                          
                    
            # DRAWING             
            self.screen.fill((0x00, 0xb0, 0x00))

            self.cardGroup.draw(self.screen)

            if self.selectionRect.width > 0 and self.selectionRect.height > 0:
                pygame.draw.rect(self.screen,(0xff,0xff,0x00),self.selectionRect,3)

            if viewhelp:
                self.screen.blit(self.helptext,self.helptextRect.topleft)

            pygame.display.flip()

             
def main():
    g = DeckOfCards()
    g.mainLoop()

 
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
