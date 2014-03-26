import random, pygame, sys
from pygame.locals import *
from TriPeaks import *

class TriPeaksGUI(object):

    FPS = 30                    # Frames per second, the general speed of the program
    WINDOWWIDTH = 1000          # Window's width in pixels
    WINDOWHEIGHT = 600          # Windows' height in pixels
    CARDWIDTH = 73              # Card width in pixels
    CARDHEIGHT = 96             # Card height in pixels
    OFFSETX = CARDWIDTH/2.0     # To find the midpoint of card
    OFFSETY = CARDHEIGHT/2.0    # To find the midpoint of card
    startx = 100                # Start drawing the board cards at this point
    starty = 100                # Start drawing the board cards at this point
    GAPSIZE = 10                # Size of gap between cards in pixels
    BOARDCOLS = 10              # Number of columns of cards
    BOARDROWS = 4               # Number of rows of cards
    BGCOLOR = (255,255,255)     # White background color

    def __init__(self):

        self.game = TriPeaks()
        self.selectedCard = None    # The card selected with the mouse

        self.mousex = 0 # x coordinate of mouse event
        self.mousey = 0 # y coordinate of mouse event
        
        self.heapRect = pygame.Rect(400, 450, self.CARDWIDTH, self.CARDHEIGHT)  # Rectangle around the heap cards
        self.deckRect = pygame.Rect(100, 450, self.CARDWIDTH, self.CARDHEIGHT)  # Rectangle around the deck cards

    # Pre:  A TriPeaksGUI object has been created
    # Post: The main game function is running until the game is stopped
    # Run:  TriPeaksGUI.gameLoop()
    def gameLoop(self):
        
        global FPSCLOCK, DISPLAYSURF
        pygame.init()
        FPSCLOCK = pygame.time.Clock()  # Clock that updates the screen with the frame rate FPS
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))        # The game display surface

        pygame.display.set_caption('Tri Peaks')     # Window title
        self.initCardsPos()

        DISPLAYSURF.fill(self.BGCOLOR)  # Sets the background color

        # Main game loop
        while True: 
            
            DISPLAYSURF.fill(self.BGCOLOR)      # Draws the window
            self.drawBoard()                    # Draws the game board

            # Event handling loop
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Event when the mouse is moved
                elif event.type == MOUSEMOTION:
                    self.onMouseMove(event)
                # Event when the mouse button is down
                elif event.type == MOUSEBUTTONDOWN:
                    self.onMouseDown(event)
                # Event when the mouse button has been released
                elif event.type == MOUSEBUTTONUP:
                    self.onMouseReleased(event)

            # Calculates the time elapsed
            self.game.elapsedTime()
                
            # Redraws the screen and waits a clock tick of one frame rate
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    # Pre:  event is a pygame.event object
    # Post: If a movable card has been selected with the mouse, it follows the mouse motion
    # Run:  TriPeaksGUI.onMouseMove(event)
    def onMouseMove(self, event):
        if self.selectedCard is not None and self.game.isMovable(self.selectedCard.row, self.selectedCard.col):
            self.selectedCard.moveTo(event.pos[0]-self.OFFSETX, event.pos[1]-self.OFFSETY)

    # Pre:  event is a pygame.event object
    # Post: If a movable card has been selected with the mouse, it becomes the selected card. If the card deck
    #       is clicked, then a card is moved to the heap
    # Run:  TriPeaksGUI.onMouseDown(event)
    def onMouseDown(self, event):
        card = self.posToCard(*event.pos)
        if card is not None and self.game.isMovable(card.row, card.col):
            self.selectedCard = self.posToCard(*event.pos)
        elif self.deckRect.collidepoint(*event.pos):
            self.game.toHeap()

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

    # Pre:  A TriPeaksGUI object has been created
    # Post: The cards in the board are assigned their positions 
    # Run:  TriPeaksGUI.initCardsPos()
    def initCardsPos(self):
        # set initial card positions
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    self.game.board[row][col].cardx = self.startx + col*(self.CARDWIDTH+self.GAPSIZE) + (3-row)*self.GAPSIZE*4
                    self.game.board[row][col].cardy = self.starty + row*(0.6*self.CARDHEIGHT)

    # Pre:  A TriPeaksGUI object has been created
    # Post: The game board has been drawn
    # Run:  TriPeaksGUI.drawBoard()
    def drawBoard(self):

        # Shows game score
        font = pygame.font.SysFont("comicsansms", 32)
        scoreStr = 'Score: ' + str(self.game.score)
        scoreText = font.render(scoreStr, True, (0, 0, 0))
        DISPLAYSURF.blit(scoreText, (20, 20))

        # Shows player moves
        moveStr = 'Moves: ' + str(self.game.moves)
        moveText = font.render(moveStr, True, (0, 0, 0))
        DISPLAYSURF.blit(moveText, (400, 20))

        # Shows game time elapsed
        timeStr = 'Time : ' + str(int(self.game.finaltime))
        timeText = font.render(timeStr, True, (0, 0, 0))
        DISPLAYSURF.blit(timeText, (800, 20))

        # Show quit command
        font = pygame.font.SysFont("comicsansms", 18)
        quitStr = 'Press ESC to quit'
        quitText = font.render(quitStr, True, (0, 0, 0))
        DISPLAYSURF.blit(quitText, (800, 550))
        
		# shows cards left
    	cardsleftStr = 'Cards left : ' + str(int(self.game.deckSize()))
        cardsleftText = font.render(cardsleftStr, True, (0, 0, 0))
        DISPLAYSURF.blit(cardsleftText, (20, 550))

        # Shows deck
        if self.game.deckSize() > 0:
            DISPLAYSURF.blit(pygame.image.load('panda.png'), (100, 450))

        # Shows heap
        for (i, card) in enumerate(self.game.heap):
            cardImg = pygame.image.load(card.img)
            DISPLAYSURF.blit(cardImg, (400, 450))
        
        # Shows cards in board
        for row in range(self.BOARDROWS):
            for col in range(self.BOARDCOLS):
                if self.game.board[row][col] is not None:
                    if self.game.isMovable(row,col):
                        cardImg = pygame.image.load(self.game.board[row][col].img).convert()
                    else:
                        cardImg = pygame.image.load('panda.png').convert()
                    DISPLAYSURF.blit(cardImg, (self.game.board[row][col].cardx, self.game.board[row][col].cardy))


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
    TriPeaks = TriPeaksGUI()        # Creates a new TriPeaksGUI object
    TriPeaks.gameLoop()             # Runs the game loop
