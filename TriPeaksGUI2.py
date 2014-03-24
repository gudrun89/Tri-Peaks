import random, pygame, sys
from pygame.locals import *
from TriPeaks import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 1000 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
CARDWIDTH = 73 # size of box height & width in pixels
CARDHEIGHT = 96
OFFSETX = CARDWIDTH/2.0
OFFSETY = CARDHEIGHT/2.0
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDCOLS= 10 # number of columns of icons
BOARDROWS = 4 # number of rows of icons

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = WHITE



def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    cardx = 200
    cardy = 200

    mouseDown = False
    mouseClicked = False
    pygame.display.set_caption('Tri Peaks')

    TriPeaksGame = TriPeaks()

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(cardx,cardy)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseDown = True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        #game logic
        if mouseDown and isOnCard(mousex,mousey, cardx,cardy):
            cardx = mousex - OFFSETX
            cardy = mousey - OFFSETY
        if mouseClicked and isOnCard(mousex,mousey,cardx,cardy):
            cardx = mousex - OFFSETX
            cardy = mousey - OFFSETY
            mouseDown = False
            mouseClicked = False
            
        
    # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isOnCard(x,y, cx, cy):
    if x > (cx-10) and x < (cx + CARDWIDTH+10):
        if y > (cy-10) and y < (cy + CARDHEIGHT+10):
            return True
    return False


def drawBoard(startx,starty):
    cardImg = pygame.image.load('panda.png')
    #for row in range(BOARDROWS):
    #    for col in range(BOARDCOLS):    
    #        DISPLAYSURF.blit(cardImg, (startx + col*(CARDWIDTH+GAPSIZE), starty + row*(0.6*CARDHEIGHT)))
    DISPLAYSURF.blit(cardImg, (startx, starty))


def getCardAtPos(x,y):
    pass
    


if __name__ == '__main__':
    main()
