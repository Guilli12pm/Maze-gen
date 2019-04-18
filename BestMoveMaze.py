from Maze import maze
import random
from Maze import bcolors
import time

def game_result(height,width,board):
    game = Mazeboards(height,width,board)
    game.board_initializer()
    while game.exit():
        game.next_turn()
    return (game.move,game.move_pattern)

class Mazeboards:
    # 0 = nothing
    # 1 = wall
    # 2 = player
    # 3 = start
    # 4 = end

    def __init__(self,height,width,start_height,end_height,board):
        self.height = height
        self.width = width
        self.board = board
        self.start = None
        self.end = None
        self.player = None
        self.move = 0
        self.previous_move = None
        self.move_pattern = []
    
    def board_initializer(self):
        """ Initializes the board """

        start = random.choice([i for i in range(1,self.height-1)])
        end = random.choice([i for i in range(1,self.height-1)])
        while end == start:
            end = random.choice([i for i in range(1,self.height-1)])

        self.start = (start,0)
        self.end = (end,self.width)

        self.board[end][self.width] = 4

        self.player = [start,0]
        self.board[start][0] = 3
    

    def printboard(self):
        for row in self.board:
            for ele in row:
                if ele == 1: print(bcolors.WARNING +"▉"+bcolors.ENDC,end="")
                elif ele == 0: print(bcolors.OKBLUE +"▉"+bcolors.ENDC,end="")
                elif ele == 3: print(bcolors.OKGREEN +"▉"+bcolors.ENDC,end="")
                elif ele == 4: print(bcolors.FAIL +"▉"+bcolors.ENDC,end="")
                elif ele == 2: print(bcolors.PLAY +"▉"+bcolors.ENDC,end="")
            print()

    def move_position(self,di,dj):
        if self.player[1] == 0 and self.player[0] == self.start[0]:
            if di == -1:
                return False
        if self.board[self.player[0] + di][self.player[1] + dj] == 1:
            return False

        if self.board[self.player[0] + di][self.player[1] + dj] == 3:
            return False
        return True
    
    def next_turn(self):
        if not self.next_to_exit():
            x = random.choice(["up","down","left","right"])

            while x == self.previous_move:
                x = random.choice(["up","down","left","right"])

            if x == "up":
                di,dj = (-1,0)
            elif x == "left":
                di,dj = (0,-1)
            elif x == "down":
                di,dj = (1,0)
            elif x == "right":
                di,dj = (0,1)
            
            neighbours = [self.move_position(-1,0),self.move_position(0,-1),self.move_position(1,0),self.move_position(0,1)]

            if x == "up" and self.move_position(di,dj):
                self.previous_move = "down"
            elif x == "down" and self.move_position(di,dj):
                self.previous_move = "up"
            elif x == "left" and self.move_position(di,dj):
                self.previous_move = "right"
            elif x == "right" and self.move_position(di,dj):
                self.previous_move = "left"

            if neighbours.count(False) == 3: self.previous_move = None

        else:
            di,dj = (0,1)

        if self.move_position(di,dj):
            self.move_pattern.append(self.didj_to_what(di,dj))

            self.move += 1 

            self.board[self.player[0]][self.player[1]] = 0
            self.player[0] += di
            self.player[1] += dj
            self.board[self.start[0]][0] = 3
            self.board[self.player[0]][self.player[1]] = 2

    def next_to_exit(self):
        if self.player[0] + 0 == self.end[0] and  self.player[1] + 1 == self.end[1]:
            return True
        return False

    def exit(self):
        if self.player[0] == self.end[0] and self.player[1] == self.end[1]:
            return False
        return True

    def didj_to_what(self,di,dj):
        if (di,dj) == (-1,0):
            return "up"
        elif (di,dj) == (0,-1):
            return "left"
        elif (di,dj) == (1,0):
            return "down"
        elif (di,dj) == (0,1):
             return "right"

board_init = maze(10,10)
#print(game_result(10,10,board_init))

def put_into_file(height,width,board,n):
    gamefile = open("board.txt","w+")
    for row in board:
        gamefile.write(str(row))
    for i in range(n):
        number,moves = game_result(height,width,board)
        filename = "test"+str(i)+".txt"
        file = open(filename,"w+")
        file.write(str(number))
        file.write("\n")
        for m in moves:
            file.write(m + "\n")
        file.close()

put_into_file(10,10,board_init,3)
