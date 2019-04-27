# TicTacToe
# 4/30/19
__author__ = 'Ben Browner'

import random as r
import copy
import sys
import time



def printBoard(board): # prints the 2D game board plus separation lines
    if str(type(board)) != "<class 'list'>" or len(board) != 3:
        return False
    else:
        print("    0   1   2  ")
        print("      ┃   ┃     ")
        print(f"0   {board[0][0]} ┃ {board[0][1]} ┃ {board[0][2]}  ")
        print("  ━━━━╋━━━╋━━━━")
        print(f"1   {board[1][0]} ┃ {board[1][1]} ┃ {board[1][2]}  ")
        print("  ━━━━╋━━━╋━━━━")
        print(f"2   {board[2][0]} ┃ {board[2][1]} ┃ {board[2][2]}  ")
        print("      ┃   ┃     ")



def gameWon(board, isComp=False): # determine if someone has won the game EFFICENCY MODE
    r = ([''.join(i).lower() for i in board] + [''.join(i).lower() for i in zip(*board[::-1])])
    r.append(''.join([board[i][i].lower() for i in range(len(board))]))
    r.append(''.join([board[2-i][i].lower() for i in range(len(board))]))
    if not isComp:
        if 'xxx' in r or 'ooo' in r: return True
        return False
    else:
        if '111' in r:
            return 10
        if '000' in r:
            return -10
        return 0

    # TODO: I had a dream where i had to debug this code but it was a mile long and I was falling through it
    # fixme: my brain


def boardIsFull(board): # return True if no spaces remain on the board, False otherwise
    for row in board:
        if ' ' in row:
            return False
    return True

def isOpen(board, r, c): # is the space at board[r][c] open or not?
    return board[r][c] == ' '

def computerMove(board): # moves for the computer based on minimax

    class Move():
        row = 0
        col = 0

    comp_board = copy.deepcopy(board)
    # if boardIsFull(comp_board):
    #     return
    # while True:
    #     row = r.randint(0, 2)
    #     col = r.randint(0, 2)
    #     if isOpen(comp_board, row, col):
    #         break

    def minimax(board, depth, isMax):
        score = gameWon(board, True)

        if score == 10 or score == -10:
            return score

        if boardIsFull(board):
            return 0

        if isMax:
            best = -1000

            for x in range(3):
                for y in range(3):
                    if board[x][y] == ' ':
                        board[x][y] = '1'
                        best = max(best, minimax(board, depth+1, (not isMax)))
                        board[x][y] = ' '

            return best
        else:
            best = 1000

            for x in range(3):
                for y in range(3):
                    if board[x][y] == ' ':
                        board[x][y] = '0'
                        best = min(best, minimax(board, depth+1, (not isMax)))
                        board[x][y] = ' '

            return best

    def findBestMove(board):

        bestVal = -1000
        bestMove = Move()
        bestMove.row = -1
        bestMove.col = -1

        for x in range(3):
            for y in range(3):
                if board[x][y] == ' ':
                    board[x][y] = '1'

                    moveVal = minimax(board, 0, False)

                    board[x][y] = ' '

                    if moveVal > bestVal:
                        bestMove.row = x
                        bestMove.col = y
                        bestVal = moveVal

        return bestMove
    bestMove = Move()
    bestMove = findBestMove(comp_board)
    return (bestMove.row, bestMove.col)

def compVScomp(play):
    print(f'Playing {play} times')
    score = [0, 0, 0]
    for i in range(play):
        cboard = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]
        whoWon = ''
        while True:
            print('C1', end=' ')
            sys.stdout.flush()
            s = time.time()
            acopy = copy.deepcopy(cboard)
            for x in range(3):
                for y in range(3):
                    if acopy[x][y].lower() == 'x':
                        acopy[x][y] = '1'
                    elif acopy[x][y].lower() == 'o':
                        acopy[x][y] = '0'
            comp1 = computerMove(acopy)
            cboard[comp1[0]][comp1[1]] = 'X'
            e = time.time()
            t = e - s
            print(t, acopy)

            if gameWon(cboard):
                whoWon = '1'
                score[0] += 1
                break

            print('C2', end=' ')
            sys.stdout.flush()
            s = time.time()
            bcopy = copy.deepcopy(cboard)
            for x in range(3):
                for y in range(3):
                    if bcopy[x][y].lower() == 'o':
                        bcopy[x][y] = '1'
                    elif bcopy[x][y].lower() == 'x':
                        bcopy[x][y] = '0'
            comp2 = computerMove(bcopy)
            cboard[comp2[0]][comp2[1]] = 'O'
            e = time.time()
            t = e - s
            print(t, bcopy)


            if gameWon(cboard):
                whoWon = '0'
                score[1] += 1
                break

            if boardIsFull(cboard):
                whoWon = 'd'
                score[2] += 1
                break

        print('0'*(3-len(str(i+1))) + str(i+1), '> ', end='')
        if whoWon == '1':
            print('Computer 1 won against Computer 2')
        elif whoWon == '0':
            print('Computer 2 won against Computer 1')
        elif whoWon == 'd':
            print('Comp 1 and Comp 2 drawed')
    print(f'Score: Comp1 ({score[0]}) | Comp2 ({score[1]}) | Draws ({score[2]})')



def main(): # main method for the tictactoe.py application
    print('* Welcome to Tic-Tac-Toe *')
    # compVScomp(50)
    first = False
    score = [0, 0, 0]
    while True:
        isPlayerTurn = True
        board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]
        if first:
            play = input('Play Again? (Y/N) ').lower()
            if play == 'n':
                break
            else:
                if play != 'y':
                    print('Invalid Input, only input Y or N')
                    continue
        first = True
        player = input('Select player (O/X): ').lower()
        if not (player == 'o' or player == 'x'):
            print('Only input O or X')
            continue
        computer = ('x' if player == 'o' else 'o')
        print('Player is', player.upper(), '| Computer is', computer.upper())
        print(player.upper(), 'is first')
        while True:
            printBoard(board)
            if isPlayerTurn:
                print('# to quit')
                select = input('Input row then column (ei. 20): ')
                if select == '#':
                    print('~' * 30)
                    break
                select = select.replace(' ', '')
                # For the sake of your program
                if len(select) == 2 and select.isdigit() and select[0] in '012' and select[1] in '012':
                    row = int(select[0])
                    col = int(select[1])
                    if isOpen(board, row, col):
                        board[row][col] = player.upper()
                    else:
                        print('Space is already filled')
                        continue
                    print('Player moves to', row, col)
                else:
                    print('Invalid Input')
                    continue
            else:
                bcopy = copy.deepcopy(board)
                for x in range(3):
                    for y in range(3):
                        if bcopy[x][y].lower() == computer:
                            bcopy[x][y] = '1'
                        elif bcopy[x][y].lower() == player:
                            bcopy[x][y] = '0'
                comp = computerMove(bcopy)
                board[comp[0]][comp[1]] = computer.upper()
                print('Computer moves to', comp[0], comp[1])
            if gameWon(board):
                printBoard(board)
                if isPlayerTurn:
                    score[0] += 1
                else:
                    score[1] += 1
                print(f'The {(f"Player ({player})" if isPlayerTurn else f"Computer ({computer})")} Won!')
                print(f'Scores: Player {score[0]} | Computer {score[1]} | Draw {score[2]}')
                score[2] += 1
                print('~'*30)
                break
            if boardIsFull(board):
                printBoard(board)
                print('Draw!')
                print(f'Scores: Player {score[0]} | Computer {score[1]} | Draw {score[2]}')
                print('~' * 30)
                break
            isPlayerTurn = (False if isPlayerTurn else True)

if __name__ == '__main__':
    main()