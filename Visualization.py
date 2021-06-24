
from typing import List

import pygame, sys, random
from pygame.locals import *
import DFS
import A_star
BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3 # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 540
WINDOWHEIGHT = 540
FPS = 50
BLANK = None

#                 R    G    B
DARKRED =       (  168, 8,   14)
ORANGE =        (  255, 177,   40)
LIGHTRED =      (  255, 85,   85)

BGCOLOR = DARKRED
TILECOLOR = ORANGE
TEXTCOLOR = DARKRED
BORDERCOLOR = LIGHTRED
BASICFONTSIZE = 40
FONT2 = 20
MESSAGECOLOR = ORANGE


XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
## setting the goal state for the puzzle
GoalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

#################### TEST CASES #######################
start_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
#start_state = [3, 1, 2, 0, 4, 5, 6, 7, 8]
#start_state = [0, 8, 7, 6, 5, 4, 3, 2, 1]

### setting the start state for each algorithm
### solving the puzzle with either A* or DFS
print("Start state: ",start_state)
DFS.setStartState(start_state)
print("Solution using DFS:")
DFS.main()
A_star.setStartState(start_state)
print("\nSolution using A*: ")
A_star.main()

###main funcion for the output visualization
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NUMBERSFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, NEW2_SURF, NEW2_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.SysFont('verdana', BASICFONTSIZE)
    NUMBERSFONT = pygame.font.Font('freesansbold.ttf', FONT2)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 520, WINDOWHEIGHT - 440)
    NEW_SURF,   NEW_RECT   = makeText('DFS', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 520, WINDOWHEIGHT - 470)
    NEW2_SURF,   NEW2_RECT   = makeText('A*', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 520, WINDOWHEIGHT - 500)

    mainBoard = to_matrix(start_state,3)
    solutionSeq = to_matrix(GoalState,3)
    SOLVEDBOARD = solutionSeq
    moves = []
    allMoves = []
    while True: 
        slideTo = None 
        msg = 'CHOOSE AN ALGORITHM TO SOLVE' 
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):# clicked on DFS button
                        moves = DFS.moves
                        allMoves = []
                    elif NEW2_RECT.collidepoint(event.pos):# clicked on A* button
                        moves = A_star.movements
                        allMoves = []
        if moves is None:
            msg = 'No solution!'
            drawBoard(mainBoard, msg)
        elif moves ==[None]:
            msg = 'The start is the goal!'
            drawBoard(mainBoard, msg)
        else:
            while  moves:
                m = moves.pop()
                if m == 'l':
                    slideTo = LEFT
                if m == 'u':
                    slideTo = UP
                if m == 'r':
                    slideTo = RIGHT
                if m == 'd':
                    slideTo = DOWN
                #Tiles movement animation during solving    
                slideAnimation(mainBoard, slideTo, 'Solving.....', 7) 
                makeMove(mainBoard, slideTo)
                allMoves.append(slideTo)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): 
        terminate() 
    for event in pygame.event.get(KEYUP): 
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event) 

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == 0:
                return (x, y)

def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == DOWN:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == UP:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tile x and tile y, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = NUMBERSFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(NEW2_SURF, NEW2_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    #This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)
    if direction == DOWN:
        movex = blankx
        movey = blanky + 1
    elif direction == UP:
        movex = blankx
        movey = blanky - 1
    elif direction == RIGHT:
        movex = blankx + 1
        movey = blanky
    elif direction == LEFT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

#The visualiztation program requires the input to be in 2D form so here
#We take the 1D inputs and transform them to 2D
def to_matrix(l, n):
	X = [l[i:i+n] for i in range(0, len(l), n)]
	return [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == DOWN:
            oppositeMove = UP
        elif move == UP:
            oppositeMove = DOWN
        elif move == LEFT:
            oppositeMove = RIGHT
        elif move == RIGHT:
            oppositeMove = LEFT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()