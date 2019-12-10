# /*
# * Part 3: Finish this implementation of a 2048 game.
# *
# * https://en.wikipedia.org/wiki/2048_(video_game)
# *
# * The player is provided a 4x4 grid of numbers, each being a power of two (2, 4, 8, 16,
# 32, 64, 128...)
# * The player may make a move LEFT, RIGHT, UP, or DOWN, which causes all numbered
# tiles to slide in that direction.
# * If a tile slides into a tile having the same number, they combine into one tile
# containing the sum of the two tiles.
# * A newly combined tile does not combine with other tiles.
# * Every time the player makes a move, a new "2" tile is spawned at a random location
# on the board.
# *
# * Example: (zeroes denote empty spaces and are excluded below)
# * 0 1 2 3
# * ------------- ------------- -------------
# * 0 | | | | | | | | |*2| <-new tile | | | | |
# * ------------- ------------- -------------
# * 1 | 4| 2| 2| 8| (2s combine) | 4| 4| 8| | | |*2| | | <- new tile
# * ------------- -- LEFT --> ------------- -- DOWN --> -------------
# * 2 |16| 4| 2| 4| |16| 4| 2| 4| | 4| | 8| 2|
# * ------------- ------------- (4s combine) -------------
# * 3 | | | | | | | | | | |16| 8| 2| 4|
# * ------------- ------------- -------------
# *
# * The game is over when no move the user can make will change the state of the board.
# * If making a move does not result in any changes, the move isn't valid, and no new piece is
# spawned
# *
# * If you have time remaining, try taking on some additional functionality (pick one or
# more of the following):
# * -- Keep track of score (every time two tiles merge, add the combined value of the tiles
# to the score)
# * -- Implement an "undo" action
# * -- Implement an AI to recommend moves and/or play the game by itself
# */

import random
import copy

class Game2048(object):
    def __init__(self):
        self.direction = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.height = 4
        self.width = 4
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.old_board = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def render(self):
        divider = '________________________'
        print(divider)
        for i in range(self.height):
            print('|', end='')
            for j in range(self.width):
                print(' '*2, self.board[i][j], '|', end='')

            print('\n')
            print(divider)

    def getMoveInput(self):
        user_say = input("Which direction would you like to move? (WASD:W=up,A=left,S=down,D=right) ")
        try:
            if user_say == 'w': return self.direction[0]
            elif user_say == 's': return self.direction[1]
            elif user_say == 'a': return self.direction[2]
            elif user_say == 'd': return self.direction[3]
            elif user_say == 'undo': 
                self.board = self.old_board
                self.render()
                self.getMoveInput()
            else: 
                print('Invalid input')
                self.getMoveInput()
        except:
            print("Exception thrown in get move input, try again(check input): ")
            self.getMoveInput()
        

    def clearBoard(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.board[1][1] = 2
        self.board[2][3] = 2
        self.old_board = self.board

    def checkBoard(self):
        if self.checkValidCell():
            return True
        if self.checkMerge():
            return True
        return False

    def checkValidCell(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return True
        return False

    def checkMerge(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):     
                if i>0 and self.board[i][j] == self.board[i-1][j]:
                    return True
                if j>0 and self.board[i][j] == self.board[i][j-1]:
                    return True
        return False

    def randomPut(self):
        row, col = len(self.board), len(self.board[0])
        x = random.randint(0, row-1)
        y = random.randint(0, col-1)
        while self.board[x][y] != 0:
            x = random.randint(0, row-1)
            y = random.randint(0, col-1)
        self.board[x][y] = 2
        
    def merge(self, choose):
        valid = self.slide(choose)
        
        valid2 = 0
        row, col = len(self.board), len(self.board[0])
        if choose == 'UP':
            for i in range(1, row):
                for j in range(col):
                    if self.board[i][j] == 0:
                        continue
                    if self.board[i][j] == self.board[i-1][j]:
                        self.board[i-1][j] *= 2
                        self.board[i][j] = 0
                        valid = 1
        elif choose == 'DOWN':
            for i in range(0, row-1):
                for j in range(col):
                    if self.board[i][j] == 0:
                        continue
                    if self.board[i][j] == self.board[i+1][j]:
                        self.board[i+1][j] *= 2
                        self.board[i][j] = 0
                        valid = 1
        elif choose == 'LEFT':
            for i in range(row):
                for j in range(1, col):
                    if self.board[i][j] == 0:
                        continue
                    if self.board[i][j] == self.board[i][j-1]:
                        self.board[i][j-1] *= 2
                        self.board[i][j] = 0
                        valid = 1
        elif choose == 'RIGHT':
            for i in range(row):
                for j in range(0, col-1):
                    if self.board[i][j] == 0:
                        continue
                    if self.board[i][j] == self.board[i][j+1]:
                        self.board[i][j+1] *= 2
                        self.board[i][j] = 0
                        valid = 1
        
        noob = self.slide(choose)
        if valid or valid2:
            self.randomPut()

    def slide(self, choose):
        row, col = len(self.board), len(self.board[0])
        valid = 0
        if choose == 'UP':
            for c in range(col):
                r1, r2 = 0, 0
                while r2 < row:
                    if self.board[r2][c] == 0:
                        r2 += 1
                    else:
                        self.board[r1][c] = self.board[r2][c]
                        r1 += 1
                        r2 += 1
                        if r1 != r2:
                            valid = 1
                while r1 < row:
                    self.board[r1][c] = 0
                    r1 += 1
        elif choose == 'DOWN':
            for c in range(col):
                r1, r2 = row-1, row-1
                while r2 >= 0:
                    if self.board[r2][c] == 0:
                        r2 -= 1
                    else:
                        self.board[r1][c] = self.board[r2][c]
                        r1 -= 1
                        r2 -= 1
                        if r1 != r2:
                            valid = 1
                while r1 >= 0:
                    self.board[r1][c] = 0
                    r1 -= 1
        elif choose == 'LEFT':
            for r in range(row):
                c1, c2 = 0, 0
                while c2 < col:
                    if self.board[r][c2] == 0:
                        c2 += 1
                    else:
                        self.board[r][c1] = self.board[r][c2]
                        c1 += 1
                        c2 += 1
                        if c1 != c2:
                            valid = 1
                while c1 < col:
                    self.board[r][c1] = 0
                    c1 += 1
        elif choose == 'RIGHT':
            for r in range(row):
                c1, c2 = col-1, col-1
                while c2 >= 0:
                    if self.board[r][c2] == 0:
                        c2 -= 1
                    else:
                        self.board[r][c1] = self.board[r][c2]
                        c1 -= 1
                        c2 -= 1
                        if c1 != c2:
                            valid = 1
                while c1 >= 0:
                    self.board[r][c1] = 0
                    c1 -= 1
        
        return valid

    # // Things to remember:
    # // - Sliding
    # // - Merging
    # // - Spawning a new 2 (only after valid moves)
    # // - Detecting the end of the game
    def play(self):
        self.clearBoard()
        while True:
            self.render()
            choose = self.getMoveInput()
            self.old_board = copy.deepcopy(self.board)
            if self.checkBoard():
                self.merge(choose)
                self.old_board 

Game2048().play()


