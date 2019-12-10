# Part 3: Implement the board game Bridges and Bombs.

#     Play an online version of the game here:
#       https://jasonhenline.github.io/bridges-and-bombs

#     This game is played on an 9x9 board of squares between two players called X
#     and O. X plays first and then the players alternate taking turns. On their
#     turn a player claims an empty square.

#     # Bridges #

#     The goal for each player is to construct a bridge of claimed squares that
#     spans from one side of the board to the opposite side.

#     A bridge is a set of contiguous squares, where squares are considered
#     contiguous if they are neighbors either horizontally or vertically.

#     X must construct a bridge between the left and right sides of the board, and
#     O must construct a bridge between the top and bottom sides of the board.

#     If a player claims a square that completes their required edge-spanning
#     bridge and the bridge survives any bomb explosions, that player wins the
#     game.

#     # Bombs #

#     If a claimed square has no vertical or horizontal neighbors belonging to the
#     same player, it becomes a bomb. A bomb starts with a countdown timer of 4 and
#     after each player's turn the timer value decreases by 1. If a bomb timer
#     reaches zero, the bomb explodes, clearing its square and its four neighbor
#     squares.

#     Bombs are created each turn after any bomb explosions are resolved, so each
#     user's turn goes like this:

#      1. The current player claims an empty square.
#      2. Any bombs belonging to the player who just moved in neighboring squares
#         of the claimed square are defused (their timers are set to undefined and
#         they become regular claimed squares).
#      3. All bomb timers are decreased by 1.
#      4. All bombs with timer equal to zero explode, clearing their square and
#         their neighbor squares.
#      5. Any claimed square with no neighbors belonging to the same player is
#         converted to a bomb with timer set to 4, if it is not already a bomb.
#      6. If the claimed square survived the bomb explosions and it completes the
#         user's bridge, the user wins the game.
#      7. If there are no empty spaces left on the board, the next player has no
#         legal moves, so the player who just played wins the game.

#     # Extra Credit #
#     - Implement a computer player that always makes a valid move
#     - Implement a computer player that makes strategic move

import copy
import os

SIZE = 9
TIMER_R = ['-4', '-3', '-2', '-1']
TIMER_B = ['4', '3', '2', '1']
class Game(object):
    # * A board square.
    # *
    # * Contains the piece on the square an the timer.
    # *
    # * A negative timer value indicates that there is no timer.
    def __init__(self):
        self.board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
        self.winner = 0 # 0:no, 1:red, 2:black


    def render(self):
        print("        a    b    c    d    e    f    g    h    i")
        print("        o    o    o    o    o    o    o    o    o")
        print("     ----------------------------------------------")
        for i in range(SIZE):
            li = []
            li.append(str(i+1))
            li.append("  x | ")
            for j in range(SIZE):
                li.append(self.board[i][j])
                li.append("  | ")
            li.append(" x  ")
            print(''.join(li))
        print("     ----------------------------------------------")
        print("        o    o    o    o    o    o    o    o    o")

    def getUserMove(self, player):
        valid = False
        while not valid: 
            print('player', player, end=' ')
            choose = input(', choose a valid location: ')
            if len(choose)==2 and 'a'<=choose[0]<='i' and '1'<=choose[1]<='9':
                valid = True
        
        return int(choose[1])-1, int(ord(choose[0])-ord('a'))
    
    def checkMove(self, x, y):
        if self.board[x][y] == ' ':
            return True
        return False

    def searchNeigbor(self, x, y, player):
        if player == 'x':
            timer = TIMER_R
        elif player == 'o':
            timer = TIMER_B

        neighbor = False
        for (dx, dy) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            n_x = x + dx
            n_y = y + dy
            if 0 <= n_x < SIZE and 0 <= n_y < SIZE and (self.board[n_x][n_y] in timer or self.board[n_x][n_y]==player):
                self.board[n_x][n_y] = player
                self.board[x][y] = player
                neighbor = True
        if not neighbor:
            self.board[x][y] = timer[0]

    def activateBomb(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            n_x = x + dx
            n_y = y + dy       
            if 0 <= n_x < SIZE and 0 <= n_y < SIZE and self.board[n_x][n_y] != ' ':
                self.board[n_x][n_y] = ' '

    def decreaseBomb(self, x, y):
        for i in range(SIZE):
            for j in range(SIZE):
                if i == x and j == y:
                    continue
                if self.board[i][j] in TIMER_R: 
                    self.board[i][j] = str(int(self.board[i][j]) + 1)
                elif self.board[i][j] in TIMER_B:
                    self.board[i][j] = str(int(self.board[i][j]) - 1)
                if self.board[i][j] == '0':
                    self.board[i][j] = ' '
                    self.activateBomb(i, j)
        
    def dfs(self, i, j, player, board, res):
        if player == 'x':
            if i<0 or j<0 or i==SIZE or j==SIZE or board[i][j]!='x': 
                return 0
            res.append(j)
            board[i][j] = '#'
            if (0 in res) and (SIZE-1 in res):
                self.winner = 1
                return 1

        elif player == 'o':
            if i<0 or j<0 or i==SIZE or j==SIZE or board[i][j]!='o': 
                return 0
            res.append(i)
            board[i][j] = '#'
            if (0 in res) and (SIZE-1 in res):
                self.winner = 2
                return 1
        
        return self.dfs(i+1, j, player, board, res) or self.dfs(i, j+1, player, board, res) \
                or self.dfs(i, j-1, player, board, res) or self.dfs(i, j+1, player, board, res)
        
    def checkWin(self, player):
        win = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == player:
                    res = []
                    ori_board = copy.deepcopy(self.board)
                    win = self.dfs(i, j, player, ori_board, res)                  

    def checkFull(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == ' ':
                    return False
        return True        

    def play(self):
        player = 'x'
        while True:
            self.render()
            # // Don't accept invalid moves.
            x, y = self.getUserMove(player)
            while not self.checkMove(x, y):
                x, y = self.getUserMove(player)
        
            # // Defuse neighbor bombs belonging to the same player (set 
            # //  their timers to a negative value).
            self.searchNeigbor(x, y, player)

            # // Convert any lonely claimed squares to bombs with timer set to 4.
            # // Decrement bomb counters by 1.
            # // Explode any bombs where the timer has reached zero.
            self.decreaseBomb(x, y)

            # // Check if the current player won by making a spanning bridge.
            self.checkWin(player)

            # // If there are no empty squares left on the board, this player is the winner. 
            if self.checkFull():
                if player == 'x':
                    self.winner = 1
                if player == 'o':
                    self.winner = 2
            
            if self.winner != 0:
                if self.winner == 1:
                    print('ther winner is BLACK')
                elif self.winner == 2:
                    print('ther winner is RED')
                os._exit(1)
                
            # // Alternate players.
            if player == 'x':
                player = 'o'
            else:
                player = 'x'           

Game().play()