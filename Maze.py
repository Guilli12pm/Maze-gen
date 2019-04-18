import random
import numpy
from numpy.random import randint as rand
import matplotlib.pyplot as pyplot
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    PLAY = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def maze(width, height, complexity=.75, density=.75):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
    # Build actual maze
    Z = numpy.zeros(shape)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2 # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

class Mazeboard:
    # 0 = nothing
    # 1 = wall
    # 2 = player
    # 3 = start
    # 4 = end

    def __init__(self,height,width,mode):
        self.height = height
        self.width = width
        self.board = [None for i in range(height)]
        self.start = None
        self.end = None
        self.player = None
        self.move = 0
        self.previous_move = None
        self.mode = mode
        self.move_pattern = []
    
    def board_initializer(self):
        """ Initializes the board """
        self.board = maze(self.height,self.width)

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
        if self.mode == 0:
            x = input()
            if x in ["z","q","s","d"]:
                if x == "z":
                    di,dj = (-1,0)
                elif x == "q":
                    di,dj = (0,-1)
                elif x == "s":
                    di,dj = (1,0)
                elif x == "d":
                    di,dj = (0,1)
            else:
                di,dj = 0,0
        
        else:
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



def main():
    game = Mazeboard(20,20,1)
    game.board_initializer()
    game.printboard()
    while game.exit():
        game.next_turn()
        game.printboard()
        time.sleep(0.01)
        print(game.move)
    print("finished")
    print(game.move_pattern)
    

main()