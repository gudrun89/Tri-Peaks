from Deck import *
from Card import *
import time
import csv
import math

class TriPeaks(object):

    #Smidur
    def __init__(self):

        self.isPlaying = True

        self.boardRows = 4
        self.boardCols = 10
        
        #Stokkur leiksins
        self.deck = Deck(52)
        self.deck.shuffleCards()
        
        #2D array of cards in the board, initialized as None
        self.board = self.initBoard()
        self.dealToBoard()
        
        #Cards in the heap
        self.heap = [self.deck.cards.pop()]
    
        #Breyta sem heldur utan um stig
        self.score = 0
    
        #Breyta sem byrjar ad taka tima
        self.start_time = time.time()
        
        #Lokatimi leiks
        self.finaltime = 0.0
    
        #Breyta sem heldur utanum 'moves'
        self.moves = 0

    def initBoard(self):
        board = []
        for i in range(3):
            board.append([None for _ in range(3*(i+1))])
        board.append([None for _ in range(10)])
        return board

    # Pre:  self.deck contains a deck of cards
    # Post: 28 cards from the deck have been dealt to the board
    # Run:  TriPeaks.dealToBoard()
    def dealToBoard(self):
        ''' Deals cards from the deck to the board '''
        for i in range(3):
            self.board[i] = [self.deck.cards.pop() for _ in range(3*(i+1))]
        self.board[3] = [self.deck.cards.pop() for _ in range(10)]

    # Post: returns how many cards are left in the deck
    # Run: TriPeaks.deckSize()
    def deckSize(self):
        return len(self.deck.cards)

    # Pre:  row and col are integers
    # Post: returns true if the card at self.board[row][col] is movable
    # Run:  TriPeaks.isMovable(row,col)
    def isMovable(self, row, col):
        ''' Checks if a card in the board is movable '''
        if (row == self.boardRows-1):
            return True
        elif (row == 0):
            return (self.board[row+1][2*col] is None and self.board[row+1][2*col+1] is None)
        elif (row == 1):
            return (self.board[row+1][col+col/2] is None and self.board[row+1][col+col/2+1] is None)
        return (row == self.boardRows-1) or (self.board[row+1][col] is None and self.board[row+1][col+1] is None)
    
    # Pre:  card is a Card object
    # Post: returns True if card has a value one higher or lower than the
    #       top card on the heap
    # Run:  TriPeaks.isLegal(card)
    def isLegal(self, card):
        ''' Checks if a card move is legal '''
        if card is None:
            return False
        return abs(self.heap[-1].value - card.value)%11 == 1


    # Pre:  row and card are integers
    # Post: card no. card in row no. row has been printed to the console
    # Run:  TriPeaks.printCard(row, col)
    def printCard(self, row, card):
        if (self.board[row][card] is None):
                print '   ',
        elif (not self.isMovable(row,card)):
            print ' # ',
        else:
            print '%-3s' % (self.board[row][card]),    

    # Post: the board has been printed to the console
    # Run:  TriPeaks.printBoard()
    def printBoard(self):
        ''' Prints the board to the console '''
        print "Cards in board: \n"
        # Row 0
        for c in range(3):
            print ' '*5,
            self.printCard(0,c)
            print ' ',
        print ' '
        
        # Row 1
        print '   ',
        for c in range(6):
            if (c%2 == 0 and c>0):
                print '   ',
            self.printCard(1,c)
        print ' '

        # Row 2
        print ' ',
        for c in range(9):
            self.printCard(2,c)
        print ' '

        # Row 3
        for c in range(10):
            self.printCard(3,c)
        print ' '
        
        print '\nCard in heap: ', self.heap[-1]
        print ''
        print 'Cards left in deck:', self.deckSize()
        print 'Score: ', self.score
        print 'Moves: ', self.moves
        self.elapsedTime()
        print 'Time:', int(self.finaltime), 'seconds'

    # Pre:
    # Post: userInput contains the string input from the user
    # Run: TriPeaks.getUserInput()
    def getUserInput(self):
        ''' Handles user inputs '''
        user = ''
        while (len(user) < 1):
            user = raw_input("What is your move? ").split()
        return user

    # Pre:  cardString is a string
    # Post: removes card from board and returns it
    # Run:  TriPeaks.getBoardCard(cardString)
    def getBoardCard(self, cardString):
        ''' Finds the card cardString in the board '''
        # TODO: laga tetta fall, er bara skitamix
        for i,row in enumerate(self.board):
            for j,c in enumerate(row):
                if (c is not None and c.toString() == cardString):
                    if (self.isLegal(self.board[i][j]) and self.isMovable(i,j)):
                        self.board[i][j] = None
                        self.addScore(150)
                        self.heap.append(c) 
                        return c
                    else:
                        print "This move is not legal, try again!"
        

    # Pre:  self.deck contains at least one Card object, self.heap is a
    #       list of Card objects
    # Post: the next card in the deck is moved on top of the heap
    # Run:  TriPeaks.toHeap()
    def toHeap(self):
        ''' Moves the next card from the deck to the heap '''
        if len(self.deck.cards) > 0:
            self.heap.append(self.deck.cards.pop())

    # Pre:  self.deck contains at least one Card object
    # Post: the next card in the deck has been removed and is returned
    # Run:  TriPeaks.drawCard()
    def drawCard(self):
        ''' Draws a card from the deck '''
        self.deck.pop()

    # Pre:  self.score is an integer
    # Post: self.score has been increased by points
    # Run:  self.addScore(points)
    def addScore(self, points):
        ''' Increases the game score by points '''
        self.score += points

    # Pre:  self.start_time is a time object
    # Post: returns the time elapsed since self.start_time
    # Run:  TriPeaks.elapsedTime
    def elapsedTime(self):
        ''' Measures the time elapsed since the game started '''
        self.finaltime = time.time() - self.start_time
    

    # Post: returns true if the game is won, false otherwise
    # Run:  TriPeaks.hasWon()
    def hasWon(self):
        ''' Checks if the game is won '''
        for r,row in enumerate(self.board):
            if any(c is not None for c in self.board[r]):
                return False
        self.isPlaying = False
        return True

    # Post: returns true if there are no more moves possible, false otherwise
    # Run:  TriPeaks.hasLost()
    def hasLost(self):
        ''' Checks if the game is lost '''
        if not len(self.deck.cards) == 0:
            return False
        for r,row in enumerate(self.board):
            for c,card in enumerate(row):
                if (self.isLegal(card) and self.isMovable(r,c)):
                    return False
        self.isPlaying = False
        return True
        
    
    # Skrifar highscore i csv skra svo haegt se ad geyma highscore
    def highscoreTable(self):
        ''' Writes a highscore to a csv file '''
        scores = []
        newhighscore = False
        with open("highscores.csv") as f:
            data = csv.reader(f, delimiter = ',')
            for row in data:
                players = []
                checker = 0
                for col in row:
                    checker += 1
                    try:
                        players.append(int(col))
                        if checker == 2 and self.score > int(col):
                            newhighscore = True
                    except:
                        players.append(col)
                scores.append(players)
        
        if newhighscore and self.hasWon():
            print ''
            name = raw_input("You are one of the top 5 Tri Peaks players! Enter your name: ")
            with open("highscores.csv", "w") as csvfile:
                a = csv.writer(csvfile, delimiter = ',')
                scores.append([name, self.score, self.finaltime, self.moves])
                scores.sort(key=lambda x: x[1])
                scores.reverse()
                a.writerows(scores[0:5])

        print ''
        print "Name\t", "\tPoints", "\tTime", "\tMoves"
        print "---------------------------------------"
        for row in scores[0:5]:
            playername = row[0]
            print playername[0:6], '\t', '\t', row[1], '\t', math.ceil(float(row[2])), '\t', row[3]
        print ''

    # Responds to the user input
    def gameAction(self, userInput):
        ''' Responds to the user input '''
        if userInput[0] == "draw":
            self.toHeap()
            self.addScore(100)
            self.moves += 1
        elif userInput[0] == "move":
            '''Moves userInput[1] to heap if legal'''
            if len(userInput) == 1:
                card = self.getBoardCard(raw_input("What card do you want to move? "))
            else:
                card = self.getBoardCard(userInput[1])
            self.moves += 1
        elif userInput[0] == "move" and not self.isLegal(userInput[1]):
            print "This move is not legal."
        elif userInput[0] == "help":
            self.showRules()
        elif userInput[0] == "top5":
            self.highscoreTable()
        elif userInput[0] == "quit":
            self.quitGame()
        else:
            print "Unknown command, remember to write 'help' to view known inputs"
            print "and the rules of the game."

    # Writes out in the end of game if you have won or lost
    def gameSettlement(self):
        ''' Writes out message to the user after the game '''
        if self.hasWon():
            self.elapsedTime()
            self.addScore(self.deckSize()*150)
            print ''
            print "You won, congratulations! You are a Tri Peaks master"
            print "Your time was", self.finaltime, "seconds"
            print "and you got", self.score, "points in", self.moves, "moves."
            self.highscoreTable()
        elif self.hasLost():
            print "You lost. Practice makes perfect."

    # Post: the game rules have been printed to the terminal
    # Run:  TriPeaks.showRules()
    def showRules(self):
        ''' Prints the game rules to the terminal'''
        print """
        TRI-PEAKS RULES:
        ----------------
        The object of Tri-Peaks is to transfer all the cards from the board
        to the heap.

        You can move a card from the board that has a value one lower or
        higher than the top card on the heap if it is not covered by
        another card.

        If you run out of moves you can move a card from the deck to the
        heap and try again to move a card from the board.
        
        How to play:
            Write "draw" to draw a card from the deck
            Write "move H7" to move H7 from board to heap
            Write "help" to view this message
            Write "top5" to view the highscore table
            Write "quit" to quit the game
        """ 

    # Post: runs the game logic
    # Run:  TriPeaks.playGame()
    def playGame(self):
        ''' Plays the game '''
        self.printBoard()
        while ((not self.hasWon() and not self.hasLost()) and self.isPlaying):
            self.gameAction(self.getUserInput())
            self.printBoard()

    def quitGame(self):
        ''' Quits current game '''
        self.isPlaying = False
        
        
if __name__ == "__main__":
    game = TriPeaks()
    game.showRules()
    game.playGame()
    game.gameSettlement()

