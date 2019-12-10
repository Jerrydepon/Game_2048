import random
import copy

SIZE = 8

class Solution(object):
    def __init__(self):
        self.board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

    def initBoard(self):
        random.seed(0)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = str(random.randint(1, 5))


    def render(self):
        print("      a    b    c    d    e    f    g    h")
        print("     ----------------------------------------------")
        for i in range(SIZE):
            li = []
            li.append(str(i+1))
            for j in range(SIZE):
                li.append("  | ")
                li.append(self.board[i][j])
            li.append("  | ")
            print(''.join(li))
        print("     ----------------------------------------------")      

    def getInput(self):
        valid = False        
        while not valid:
            choose = input('choose a grid to eliminate gems: ')
            if len(choose)==2 and 'a'<=choose[0]<='h' and '1'<=choose[1]<='8':
                valid = True
            else:
                print('Invalid Input')
        return int(choose[1])-1, ord(choose[0])-ord('a')

    def checkNeighbor(self, i, j, x, y):
        if i<0 or j<0 or i==SIZE or j==SIZE or self.board[i][j]!=self.board[x][y]:
            return False
        else:
            return True

    def checkValid(self, x, y):
        valid = False
        for (dx, dy) in [(0,1), (1,0), (-1,0), (0,-1)]:
            i = x + dx
            j = y + dy
            valid = valid or self.checkNeighbor(i, j, x, y)            
        return valid

    def eliminate(self, x, y, gem, change_li, start):
        if x<0 or y<0 or x==SIZE or y==SIZE or self.board[x][y]=='0' or self.board[x][y]!=gem:
            return
        if start:
            start = False
        else:
            change_li.append((x, y))
            self.board[x][y] = '0'
        for (dx, dy) in [(0,1), (1,0), (-1,0), (0,-1)]:
            i = x + dx
            j = y + dy 
            self.eliminate(i, j, gem, change_li, start)   
        if change_li:
            return change_li    

    def sortList(self, li):
        gem_li = []
        for ele in li:
            if ele != '0':
                gem_li.append(ele)
        all_li = copy.deepcopy(gem_li)
        all_li.extend(['0']*(len(li)-len(gem_li)))
        return gem_li, all_li, all_li!=li

    def drop(self):
        dropping = False
        drop_xy = []
        change_li = []
        for j in range(SIZE): 
            for i in range(SIZE-1, -1, -1):
                if self.board[i][j] == '0':
                    li = [] 
                    for k in range(i, -1, -1):
                        li.append(self.board[k][j])
                    gems, sorted_li, change = self.sortList(li)
                    dropping = dropping or change

                    idx = 0
                    for k in range(i, -1, -1):
                        self.board[k][j] = sorted_li[idx]
                        idx += 1
                    break     
        return dropping

    def newElements(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == '0':
                    self.board[i][j] = str(random.randint(1, 5))

    def play(self):
        self.initBoard()
        while True:
            self.render()
            x, y = self.getInput()

            if not self.checkValid(x, y):
                print(('Invalid Input'))
                continue
            
            change_li = self.eliminate(x, y, self.board[x][y], [], True)
            
            while True:
                dropping = self.drop()
                self.render()
                fix_li = copy.deepcopy(change_li)
                change_li = []
                # print(fix_li)
                if not dropping:
                    break
                for (i, j) in fix_li:
                    sub_change_li = (self.eliminate(i, j, self.board[i][j], [], True))
                    if sub_change_li:
                        change_li.extend(sub_change_li)
                self.render()

            self.newElements()

Solution().play()