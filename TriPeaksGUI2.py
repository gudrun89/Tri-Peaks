import random, pygame, sys
from pygame.locals import *
from TriPeaks import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
CARDSIZE = 40 # size of box height & width in pixels
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
    pygame.display.set_caption('Tri Peaks')

    TriPeaksGame = TriPeaks()

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()   # opposite of pygame.init()
                sys.exit()
        
    # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard():
    cardImg = pygame.image.load('panda.png')
    


if __name__ == '__main__':
    main()
