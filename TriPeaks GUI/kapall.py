import random, pygame, sys
from pygame.locals import *
from TriPeaks import *
from time import time
from collections import deque

class TriPeaksGUI(object):

    # Constants:

    FPS = 30                    # Frames per second, the general speed of the program
    WINDOWWIDTH = 1000          # Window's width in pixels
    WINDOWHEIGHT = 600          # Windows' height in pixels
    CARDWIDTH = 73              # Card width in pixels
    CARDHEIGHT = 96             # Card height in pixels
    OFFSETX = CARDWIDTH/2.0     # To find the midpoint of card
    OFFSETY = CARDHEIGHT/2.0    # To find the midpoint of card
    GAPSIZE = 10                # Size of gap between cards in pixels
    BOARDCOLS = 10              # Number of columns of cards
    BOARDROWS = 4               # Number of rows of cards

    def __init__(self):
        pygame.init()
        self.setupGame()
        
    # Pre:  A TriPeaksGUI object has been created
    # Post: The main game function is running until the game is stopped
    # Run:  TriPeaksGUI.gameLoop()
    def gameLoop(self):

        global FPSCLOCK, DISPLAYSURF
       
        FPSCLOCK = pygame.time.Clock()  # Clock that updates the screen with the frame rate FPS
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))        # The game display surface

        pygame.display.set_caption('Tri Peaks')     # Window title
 
        # Main game loop
        while True: 
            
            DISPLAYSURF.blit(self.backgroundImg, (0,0))
            self.drawBoard()                    # Draws the game board

            # Event handling loop
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP and event.key == K_r:
                    self.restartGame()

                if event.type == KEYUP and event.key == K_h:
                    self.showHints = not self.showHints

                # Test: show help
                if event.type == KEYUP and event.key == K_F1:
                    self.showHelp = not self.showHelp
                # Event when the mouse is moved
                elif event.type == MOUSEMOTION:
                    self.onMouseMove(event)
                # Event when the mouse is double clicked
                elif event.type == MOUSEBUTTONDOWN and (time() - self.lastClickTime < self.doubleClickInterval):
                    self.onMouseDoubleClick(event)
                # Event when the mouse button is down
                elif event.type == MOUSEBUTTONDOWN:
                    self.onMouseDown(event)
                # Event when the mouse button has been released
                elif event.type == MOUSEBUTTONUP:
                    self.onMouseReleased(event)


            self.game.elapsedTime()
            self.animateCard()

            if self.game.isPlaying:
                self.isGameOver()
            
            # Redraws the screen and waits a clock tick of one frame rate
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    # Pre:  event is a pygame.event object
    # Post: If a movable, legal card is selected with the mouse, it is moved to the heap
    # Run:  TriPeaksGUI.onMouseMove(event)
    def onMouseDoubleClick(self, event):
        card = self.posToCard(*event.pos)
        if card is None or not self.game.isMovable(card.row, card.col):
            return
        if self.game.isLegal(card):
            self.animationQueue.append((card, (self.heapRect.x, self.heapRect.y), lambda: self.game.moveToHeap(card)))
            self.cardSound.play()
            

    # Pre:  event is a pygame.event object
    # Post: If a movable card has been selected with the mouse, it follows the mouse motion
    # Run:  TriPeaksGUI.onMouseMove(event)
    def onMouseMove(self, event):
        if not self.game.isPlaying:
            return
        if self.selectedCard is not None and self.game.isMovable(self.selectedCard.row, self.selectedCard.col):
            self.selectedCard.moveTo(event.pos[0]-self.OFFSETX, event.pos[1]-self.OFFSETY)

    # Pre:  event is a pygame.event object
    # Post: If a movable card has been selected with the mouse, it becomes the selected card. If the card deck
    #       is clicked, then a card is moved to the heap
    # Run:  TriPeaksGUI.onMouseDown(event)
    def onMouseDown(self, event):
        self.lastClickTime = time()
        card = self.posToCard(*event.pos)
        if card is not None and self.game.isMovable(card.row, card.col):
            self.selectedCard = self.posToCard(*event.pos)
        elif self.deckRect.collidepoint(*event.pos) and len(self.game.deck.cards) > 0:
            self.animationQueue.append((self.game.deck.cards[-1], (self.heapRect.x, self.heapRect.y), lambda: self.game.toHeap()))
            #self.deckToHeapCard = self.game.deck.cards[-1]
            self.cardSound.play()

    # Pre:  event is a pygame.event object
    # Post: If a legal card was selected then it moves to the heap if it collides with the heap card,
    #       otherwise the card is moved back to its position in the board
    # Run:  TriPeaksGUI.onMouseReleased(event)
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


    def animateCard(self):
        if len(self.animationQueue) == 0:
            return
        for i,triple in enumerate(self.animationQueue):
            card,dest,callback = triple
            dx = dest[0] - card.cardx
            dy = dest[1] - card.cardy
            distSq = dx**2 + dy**2
            card.moveTo(card.cardx + dx/2.0, card.cardy + dy/2.0)
            if distSq < 1:
                callback()
                del(self.animationQueue[i])
              

    def isGameOver(self):
        if self.game.hasWon():
            self.game.isPlaying = False
            self.hasWon = True
            self.rockyWinSound.play()
            
        elif self.game.hasLost():
            self.game.isPlaying = False
            self.hasLost = True
            self.sadLoseSound.play()


    def restartGame(self):
        pygame.mixer.stop()
        self.setupGame()


    def setupGame(self):
        self.game = TriPeaks()
        
        self.hasWon = False
        self.hasLost = False
        self.showHelp = False           # Help instructions shown if True
        self.showHints = False          # Legal cards shown if True
        self.selectedCard = None        # The card selected with the mouse
        self.lastClickTime = 0.0        # The time of last mouse click
        self.doubleClickInterval = 0.3  # The threshold interval between clicks in double mouse click
        self.animationQueue = []        # Cards that are moving
        self.waitingQueue = deque()     # Cards waiting to be moved

        self.mousex = 0                 # x coordinate of mouse event
        self.mousey = 0                 # y coordinate of mouse event

        self.startx = 100               # Start drawing the board cards at this point
        self.starty = 100               # Start drawing the board cards at this point
        
        self.heapRect = pygame.Rect(400, 450, self.CARDWIDTH, self.CARDHEIGHT)  # Rectangle around the heap cards
        self.deckRect = pygame.Rect(100, 450, self.CARDWIDTH, self.CARDHEIGHT)  # Rectangle around the deck cards
        
        self.cardSound = pygame.mixer.Sound("card2.wav")
        self.sweepSound = pygame.mixer.Sound("sweep.wav")
        self.sadLoseSound = pygame.mixer.Sound("sadLose.wav")
        self.rockyWinSound = pygame.mixer.Sound("rocky.wav")
        self.shuffleSound = pygame.mixer.Sound("shuffle.wav")

        self.backgroundImg = pygame.image.load('woodBackground.jpg')

        self.initCardsPos()

    # Pre:  A TriPeaksGUI object has been created
    # Post: The cards in the board are assigned their positions 
    # Run:  TriPeaksGUI.initCardsPos()
    def initCardsPos(self):        
        self.shuffleSound.play()
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    card = self.game.board[row][col]
                    destx = self.startx + col*(self.CARDWIDTH+self.GAPSIZE) + (3-row)*self.GAPSIZE*4
                    desty = self.starty + row*(0.6*self.CARDHEIGHT)
                    card.cardx = self.deckRect.x
                    card.cardy = self.deckRect.y
                    self.waitingQueue.append((card, (destx,desty), lambda: self.animationQueue.append(self.waitingQueue.popleft())))
        
        self.waitingQueue[-1] = self.waitingQueue[-1][:2] + (lambda: None,)
        self.animationQueue.append(self.waitingQueue.popleft())
        
        for card in self.game.deck.cards:
            card.cardx = self.deckRect.x
            card.cardy = self.deckRect.y
        
    # Pre:  A TriPeaksGUI object has been created
    # Post: The game board has been drawn
    # Run:  TriPeaksGUI.drawBoard()
    def drawBoard(self):

        # Shows game score
        font = pygame.font.SysFont("comicsansms", 32)
        scoreStr = 'Score: ' + str(self.game.score)
        scoreText = font.render(scoreStr, True, (255, 255, 255))
        DISPLAYSURF.blit(scoreText, (20, 20))

        # Shows player moves
        moveStr = 'Moves: ' + str(self.game.moves)
        moveText = font.render(moveStr, True, (255, 255, 255))
        DISPLAYSURF.blit(moveText, (400, 20))

        # Shows game time elapsed
        timeStr = 'Time : ' + str(int(self.game.finaltime))
        timeText = font.render(timeStr, True, (255, 255, 255))
        DISPLAYSURF.blit(timeText, (800, 20))

        # Shows key information
        font = pygame.font.SysFont("comicsansms", 18)
        restartStr = 'Press R to restart'
        quitStr = 'Press ESC to quit'
        helpStr = 'Press F1 to show/hide help'
        hintStr = 'Press H to show/hide legal cards'
        restartText = font.render(restartStr, True, (255, 255, 255))
        quitText = font.render(quitStr, True, (255, 255, 255))
        helpText = font.render(helpStr, True, (255, 255, 255))
        hintText = font.render(hintStr, True, (255, 255, 255))
        DISPLAYSURF.blit(restartText, (710, 510))
        DISPLAYSURF.blit(quitText, (710, 530))
        DISPLAYSURF.blit(helpText, (710, 550))
        DISPLAYSURF.blit(hintText, (710, 570))

        # shows cards left
        cardsleftStr = 'Cards left : ' + str(int(self.game.deckSize()))
        cardsleftText = font.render(cardsleftStr, True, (255, 255, 255))
        DISPLAYSURF.blit(cardsleftText, (20, 550))

        # Shows help if help is "on"
        if self.showHelp:
            font = pygame.font.SysFont("comicsansms", 18)
            helpStr1 = 'TRI-PEAKS RULES:'
            helpStr2 = 'Move all cards from the board to the heap.'
            helpStr3 = 'You can move cards with value +/-1 the value'
            helpStr4 = 'of the top card on the heap. You can also click'
            helpStr5 = 'on the deck to add a card to the heap.'
            helpText1 = font.render(helpStr1, True, (255, 255, 255))
            helpText2 = font.render(helpStr2, True, (255, 255, 255))
            helpText3 = font.render(helpStr3, True, (255, 255, 255))
            helpText4 = font.render(helpStr4, True, (255, 255, 255))
            helpText5 = font.render(helpStr5, True, (255, 255, 255))
            DISPLAYSURF.blit(helpText1, (600, 400))
            DISPLAYSURF.blit(helpText2, (600, 420))
            DISPLAYSURF.blit(helpText3, (600, 440))
            DISPLAYSURF.blit(helpText4, (600, 460))
            DISPLAYSURF.blit(helpText5, (600, 480))

        # Shows heap
        for (i, card) in enumerate(self.game.heap):
            cardImg = pygame.image.load(card.img)
            if not self.game.isPlaying:
                DISPLAYSURF.blit(cardImg, (400, 450), special_flags = BLEND_MULT)
            else:
                DISPLAYSURF.blit(cardImg, (400, 450))


        # Shows animated cards
        for triple in self.animationQueue:
            cardImg = pygame.image.load(triple[0].img)
            DISPLAYSURF.blit(cardImg, (triple[0].cardx, triple[0].cardy))
            
        
        # Shows cards in board
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    if self.game.isMovable(row,col):
                        cardImg = pygame.image.load(self.game.board[row][col].img)
                    else:
                        cardImg = pygame.image.load('panda2.png')
                    if not self.game.isPlaying:
                        DISPLAYSURF.blit(cardImg, (self.game.board[row][col].cardx, self.game.board[row][col].cardy), special_flags = BLEND_MULT)
                    elif self.showHints and self.game.isMovable(row,col) and not self.game.isLegal(self.game.board[row][col]):
                        DISPLAYSURF.blit(cardImg, (self.game.board[row][col].cardx, self.game.board[row][col].cardy), special_flags = BLEND_MULT)
                    else:
                        DISPLAYSURF.blit(cardImg, (self.game.board[row][col].cardx, self.game.board[row][col].cardy))

        # Shows deck
        if self.game.deckSize() > 0:
            DISPLAYSURF.blit(pygame.image.load('panda2.png'), (100, 450))

        # Winning message
        if self.hasWon:
            font = pygame.font.SysFont("comicsansms", 70)
            winStr = 'YOU WON!!!'
            winText = font.render(winStr, True, (0,255,0))
            DISPLAYSURF.blit(winText, (300, 200))
            
        # Losing message
        if self.hasLost:
            font = pygame.font.SysFont("comicsansms", 70)
            font2 = pygame.font.SysFont("comicsansms", 50)
            loseStr = 'YOU LOST!!!'
            againStr = 'Press R to start a new game'
            loseText = font.render(loseStr, True, (255,0,0))
            againText = font2.render(againStr, True, (255,0,0))
            DISPLAYSURF.blit(loseText, (300, 200))
            DISPLAYSURF.blit(againText, (200, 270))


    # Pre:  row and col are integers
    # Post: Returns the left, top coordinates of the card at row, col
    # Run:  TriPeaksGUI.cardToPos(row, col)
    def cardToPos(self, row, col):
        left = self.startx + col * (self.CARDWIDTH + self.GAPSIZE) + (3-row)*self.GAPSIZE*4
        top = self.starty + row * 0.6*(self.CARDHEIGHT)
        return (left, top)


    # Pre:  x and y are integers
    # Post: Returns the card at window coordinates (x,y), returns None if there is no card there
    # Run:  TriPeaksGUI.posToCard(x,y)
    def posToCard(self, x,y):
        for cardCol in range(self.BOARDCOLS):
            for cardRow in range(self.BOARDROWS):
                left, top = self.cardToPos(cardRow, cardCol)
                cardRect = pygame.Rect(left, top, self.CARDWIDTH, self.CARDHEIGHT)
                if cardRect.collidepoint(x, y) and self.game.isMovable(cardRow, cardCol):
                    return self.game.board[cardRow][cardCol]
        return None


if __name__ == '__main__':
    kapall = TriPeaksGUI()        # Creates a new TriPeaksGUI object
    kapall.gameLoop()             # Runs the game loop
