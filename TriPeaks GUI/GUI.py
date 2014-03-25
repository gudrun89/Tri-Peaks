import random, pygame, sys
from pygame.locals import *
from TriPeaks import *

class TriPeaksGUI(object):

    FPS = 30 # frames per second, the general speed of the program
    WINDOWWIDTH = 1000 # size of window's width in pixels
    WINDOWHEIGHT = 600 # size of windows' height in pixels
    CARDWIDTH = 73 # size of card width in pixels
    CARDHEIGHT = 96 # size of card height in pixels
    OFFSETX = CARDWIDTH/2.0    # to find the midpoint of card
    OFFSETY = CARDHEIGHT/2.0   # to find the midpoint of card
    startx = 100   # start drawing cards at this point
    starty = 100   # start drawing cards at this point
    GAPSIZE = 10 # size of gap between cards in pixels
    BOARDCOLS = 10 # number of columns of cards
    BOARDROWS = 4 # number of rows of cards
    BGCOLOR = (255,255,255) # white background color

    def __init__(self):

        self.game = TriPeaks()
        self.selectedCard = None

    def gameLoop(self):
        
        global FPSCLOCK, DISPLAYSURF
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))

        self.mousex = 0 # x coordinate of mouse event
        self.mousey = 0 # y coordinate of mouse event
        self.heapRect = pygame.Rect(400, 450, self.CARDWIDTH, self.CARDHEIGHT)
        self.deckRect = pygame.Rect(100, 450, self.CARDWIDTH, self.CARDHEIGHT)
        
        pygame.display.set_caption('Tri Peaks')
        self.initCardsPos()

        DISPLAYSURF.fill(self.BGCOLOR)  # sets the background color

        while True: # main game loop
            
            DISPLAYSURF.fill(self.BGCOLOR) # drawing the window
            self.drawBoard()
            
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    self.onMouseMove(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.onMouseDown(event)
                elif event.type == MOUSEBUTTONUP:
                    self.onMouseReleased(event)

                
            
        # Redraw the screen and wait a clock tick.
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def onMouseMove(self, event):
        if self.selectedCard is not None and self.game.isMovable(self.selectedCard.row, self.selectedCard.col):
            self.selectedCard.moveTo(event.pos[0]-self.OFFSETX, event.pos[1]-self.OFFSETY)


    def onMouseDown(self, event):
        card = self.posToCard(*event.pos)
        if card is not None and self.game.isMovable(card.row, card.col):
            self.selectedCard = self.posToCard(*event.pos)
            print self.selectedCard
        elif self.deckRect.collidepoint(*event.pos):
            self.game.toHeap()


    def onMouseReleased(self, event):
        if self.selectedCard is not None:
            x, y = self.cardToPos(self.selectedCard.row, self.selectedCard.col)
            selx, sely = event.pos
            selCardRect = pygame.Rect(selx, sely, self.CARDWIDTH, self.CARDHEIGHT)
            if selCardRect.colliderect(self.heapRect) and self.game.isLegal(self.selectedCard):
                self.game.moveToHeap(self.selectedCard)
            else:
                self.selectedCard.moveTo(x,y)
            self.selectedCard = None


    def initCardsPos(self):
        # set initial card positions
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    self.game.board[row][col].cardx = self.startx + col*(self.CARDWIDTH+self.GAPSIZE) + (3-row)*self.GAPSIZE*4
                    self.game.board[row][col].cardy = self.starty + row*(0.6*self.CARDHEIGHT)


    def drawBoard(self):

        # show deck
        if self.game.deckSize() > 0:
            DISPLAYSURF.blit(pygame.image.load('panda.png'), (100, 450))

        # show heap
        for (i, card) in enumerate(self.game.heap):
            cardImg = pygame.image.load(card.img)
            DISPLAYSURF.blit(cardImg, (400, 450))
        
        # show cards in board
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    if self.game.isMovable(row,col):
                        cardImg = pygame.image.load(self.game.board[row][col].img).convert()
                    else:
                        cardImg = pygame.image.load('panda.png').convert()
                    #print '(', game.board[row][col].cardx, ', ', game.board[row][col].cardy
                    DISPLAYSURF.blit(cardImg, (self.game.board[row][col].cardx, self.game.board[row][col].cardy))


    def cardToPos(self, row, col):
        # returns left, top coordinates of card
        #(startx + col*(CARDWIDTH+GAPSIZE) + (3-row)*GAPSIZE*4, starty + row*(0.6*CARDHEIGHT))
        left = self.startx + col * (self.CARDWIDTH + self.GAPSIZE) + (3-row)*self.GAPSIZE*4
        top = self.starty + row * 0.6*(self.CARDHEIGHT)
        return (left, top)


    def posToCard(self, x,y):
        # returns indices of card at coordinates (x,y)
        for cardCol in range(self.BOARDCOLS):
            for cardRow in range(self.BOARDROWS):
                left, top = self.cardToPos(cardRow, cardCol)
                #print game.board[cardRow][cardCol], left, top
                cardRect = pygame.Rect(left, top, self.CARDWIDTH, self.CARDHEIGHT)
                if cardRect.collidepoint(x, y) and self.game.isMovable(cardRow, cardCol):
                    return self.game.board[cardRow][cardCol]
        return None


if __name__ == '__main__':
    TriPeaks = TriPeaksGUI()
    TriPeaks.gameLoop()
