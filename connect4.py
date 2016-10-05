# Anthony Knight
# CS 121
# Fall 2015

from random import *
from tkinter import *


class Board:

    def __init__( self, width, height, board):
        self.ignoreEvents=True
        self.gameover = False
        self.width = width
        self.height = height
        self.array = [] #the board
        self.board = board
        self.frame = Frame(board)
        self.frame.pack(fill='both', expand='yes')
        self.quitButton = Button(self.frame, text = 'Quit', fg = 'red', command=self.quit)
        self.quitButton.pack(side=BOTTOM)
        self.newGameButton = Button(self.frame, text = 'New Game', fg='green', command=self.newGame)
        self.newGameButton.pack(side=TOP)
        self.draw = Canvas(board, width =750, height = 500, bg = 'orange', borderwidth = 15)
        self.draw.bind("<Button-1>", self.mouse)
        self.draw.pack()
        self.message = self.draw.create_text(750/2, 495, text="Connect Four")
  
        for row in range ( self.height ):
            boardRow = []
            for col in range (self.width):
                boardRow += [' ']
            self.array += [boardRow]
        
        self.circles = []
        self.colors = []
        y = 25
        for row in range(self.height):
            r = []
            x = 27
            d = 65
            colorRow = []
            for col in range(self.width):
                if row >= 0 and col >= 0:
                    r+=[self.draw.create_oval(x,y,x+d,y+d,fill='white')]
                    colorRow += ['white']
                    x+= d+44
            y+= d+10
            self.circles+= [r]
            self.colors += [colorRow]
        
        self.ignoreEvents=False
        
        
    #def __repr__ (self):
        
        #s = '' 
        #for row in range ( self.height ):
            #s += '|' #spacing character
            #for col in range (self.width):
                #s += self.array[row][col] + '|'
            #s += '\n'
            
        #s += '___' * self.width
        #s += '\n__'
        
        #for col in range (self.width):
            #s += ' ' + str(col)
        
        #return s
    
    def newGame(self):
        for row in range(0,self.height):
            for col in range(0,self.width):
                self.array[row][col] = ' '
                self.draw.itemconfig(self.circles[row][col], fill = "white")
        self.draw.itemconfig(self.message, text="Your move, friend")
        self.gameover = False
        self.ignoreEvents = False
        
    def quit(self):
        self.board.destroy()
    
    def allowsMove (self, col):
        if 0 <= col < self.width:
            if self.array[0][col] == ' ':
                return True
        return False
    
    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range( self.height ):
                if self.array[row][col] != ' ':
                    self.array[row-1][col] = ox
                    return row-1
            self.array[self.height-1][col] = ox
            return self.height-1
    
    def delMove(self, col):
        for row in range( self.height ):
            if self.array[row][col] != ' ':
                self.array[row][col] = ' '
                return
    
    def winsFor(self, ox):
        
        #horizontal win check
        for row in range(0,self.height):
            for col in range(0,self.width-3):
                if self.array[row][col] == ox and \
                   self.array[row][col+1] == ox and \
                   self.array[row][col+2] == ox and \
                   self.array[row][col+3] == ox:
                    return True
            
        #vertical win check
        for col in range (0,self.width):
            for row in range(0,self.height-3):
                if self.array[row][col] == ox and \
                   self.array[row+1][col] == ox and \
                   self.array[row+2][col] == ox and \
                   self.array[row+3][col] == ox:
                    return True
        
        #diagonal win check top right to bottom left           
        for row in range(0,self.height-3):
            for col in range(0,self.width-3):
                if self.array[row][col] == ox and \
                   self.array[row+1][col+1] == ox and \
                   self.array[row+2][col+2] == ox and \
                   self.array[row+3][col+3] == ox:
                    return True
        
        #diagonal win check bottom right to top left
        for row in range(3,self.height):
            for col in range(0,self.width-3):
                if self.array[row][col] == ox and \
                   self.array[row-1][col+1] == ox and \
                   self.array[row-2][col+2] == ox and \
                   self.array[row-3][col+3] == ox:
                    return True
    
    def isFull(self):
        for col in range (0,self.width):        
            if self.allowsMove(col):
                return False
        return True
    
    def getMove (self, ox):
        while True:
            prompt = 'Enter move for %s: ' %(ox)
            move = eval(input(prompt))
            return move
            #if len(move) == 2:
                #row = move[0]
                #col = move[1]
                #if self.moveAllow(row, col):
                    #self.addMove (row, col, ox)
                    #return
            #else:
                #print("Bad move! Try again.")
                

    

    def playGameWith( self, aiPlayer):
        player1 = 'x'
        while True:
            x = self.getMove('x')
            print(self)
            self.addMove(x, player1)
            if self.winsFor(player1):
                print("Congratulations! x wins!")
                break
            if self.isFull():
                print("It's a draw!")
                break
            oMove = aiPlayer.nextMove(self)
            self.addMove(oMove, 'o')
            if self.winsFor('o'):
                print("Congratulations! o wins!")
                break
    
    def playGUI(self, aiPlayer):
        self.aiPlayer = aiPlayer
    
    def mouse(self, event):
        if self.ignoreEvents:
            return
        if self.gameover:
            return
        self.ignoreEvents = True
        col = int(event.x/110)
        self.draw.itemconfig(self.message, text="You chose column %i" %(col+1))
        if self.allowsMove(col):
            row = self.addMove(col,'x')
            self.draw.itemconfig(self.circles[row][col], fill =  "black")
            if self.winsFor('x'):
                self.draw.itemconfig(self.message, text = "You win this time, human!")
                self.gameover = True
                return
            if self.isFull():
                self.draw.itemconfig(self.message, text = "Looks like it's a tie!")
                self.gameover = True
                return
            self.board.update()
            move = self.aiPlayer.nextMove(self)
            row = self.addMove(move, 'o')
            self.draw.itemconfig(self.circles[row][move], fill = 'red')
            if self.winsFor('o'):
                self.draw.itemconfig(self.message, text="Bested by the computer. How sad. YOU LOSE.")
                self.gameover = True
                return
            if self.isFull():
                self.draw.itemconfig(self.message, text="Looks like it's a tie!")
                self.gameover = True
                return
        else:
            self.draw.itemconfig(self.message, text="That was an invalid move. Try again.")
        self.ignoreEvents=False
            
    #def mouseRow(self, col):
        #rows = [row for row in range(self.height) if self.array[row][col] == ' ']
        #rows = max(rows)
        #return rows 
   
    
    #def hostGame(self):
        #player1 = 'x'
        #player2 = 'o'
        #currentPlayer = player1
        #while True:
            #print(self)
            #self.getMove(currentPlayer)
            #if self.winsFor(currentPlayer):
                #print("Congratulations! %s wins!" %(currentPlayer))
                #break
            #if self.isFull():
                #print("It's a draw!")
                #break
            #if currentPlayer == player1:
                #currentPlayer = player2
            #else:
                #currentPlayer = player1
    
class Player:
    
    def __init__(self, ox, ply):
        self.ox = ox
        self.ply = ply
    
    def nextPlayer(self, ox):
        if ox == 'x':
            player = 'o'
        else:
            player = 'x'
        return player
    
    def nextMove(self, board):
        moves = self.ScoreDecide(board, self.ox, self.ply)
        decision = max(moves)
        Columns = []
        for i in range(board.width):
            if moves[i] == decision:
                Columns.append(i)
        return choice(Columns)
    
    def ScoreDecide(self, board, ox, ply):
        scores = []
        for col in range(board.width):
            if board.allowsMove(col):
                board.addMove(col, ox)
                if board.winsFor(ox):
                    scores.append([100])
                elif ply == 1:
                    scores.append([50])
                else:
                    Human = self.nextPlayer(ox)
                    HumanScores = self.ScoreDecide(board, Human, ply-1)
                    bestDecision = max(HumanScores)
                    for i in bestDecision:
                        scores.append([100-i])
                board.delMove(col)
            else:
                scores.append([-1])
        return scores
    
 
 

def playWithGUI (ply):
    gameBoard = Tk()
    gameBoard.title("Connect Four Game")
    bd = Board(7, 6, gameBoard)
    aiPlayer = Player('o', ply)
    bd.playGUI(aiPlayer)
    gameBoard.mainloop()  