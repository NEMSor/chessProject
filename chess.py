

class Player():
    def __init__(self, color, pieces):
        self.color = color
        self.pieces = pieces
        pass

class Chess():
    def __init__(self, player1, player2):
        self.board = [[ '   ' for i in range(8)] for i in range(8)]
        self.players = [player1, player2]
        pass
    
    def showBoard(self):
        print('')
        print('   ','  0  ', '  1  ', '  2  ', '  3  ', '  4  ', '  5  ', '  6  ', '  7  ')
        print('')
        for y in range(8):
            #print(y, self.board[y])
            print (y, '', '|',self.board[y][0], '|',self.board[y][1], '|',self.board[y][2], '|',self.board[y][3], '|',self.board[y][4], '|',self.board[y][5], '|',self.board[y][6], '|',self.board[y][7],'|',)
            print('   ',' ---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ')
    def allPieceCoords(self):
        for a in range(2):
            for pieces in self.players[a]:
                print(pieces.desig, Cor[pieces])
            print("-")
    def setBoard(self):
        for x in range(8):
            self.board[1][x] = 'wP'+str(x)
            self.board[6][x] = 'bP'+str(x)
        for c in ['w','b']:
            if c == 'w':
                y=0
                x2 = 3
            else:
                y=7
                x2 = 4
            x = 0
            for p in ['R','N','B']:
                self.board[y][x] = c+p+str(0)
                self.board[y][-(1+x)] = c+p+str(1)
                x = x+1
            
            for p in range(2):
                self.board[y][x2] =  c+'K'+str(0)
                self.board[y][-(1+x2)] = c+'Q'+str(0)
        for a in range(2):
            for pieces in self.players[a]:
                Cor[pieces] = pieces.checkPos(game)

        pass
    def isFree(self, coords):
        return self.board[coords[0][coords[1]]]
        pass

class piece():
    def __init__(self, color="White", num=0, eliminated=False, type = "type"):
        self.color = color
        self.eliminated = eliminated
        self.type = type
        if color == 'b':
            self.opcolor = 'w'
        else:
            self.opcolor= 'b'
        self.num = num
        self.desig = type + str(num)
    def checkPos(self,game):
        self.cor = [0,0]
        self.cor[0] = 100
        self.cor[1] = 100
        if not self.eliminated:
            for y in range(8):
                if self.desig in game.board[y]:
                    self.cor[0] = y
                    for x in range(8):
                        if self.desig == game.board[y][x]:
                            self.cor[1] = x
        return self.cor
    def yMove(self, game):
        
        pass
    def xMove(self, game):
        pass
    def diagMoveCheck(self, game):
        pass
    def movement(self):
        print("ERROR!")

class pawn(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "P"
        self.desig = self.color + self.type + str(self.num)
    def movement(self, game):
        validMoves = []
        y = 0
        x = 1
        cor = self.checkPos(game)
        yT = cor[y]-1
        xT = [cor[x]-1, cor[x]+1]
        takes = [[yT,xT[0]], [yT,xT[1]]]
        for move in takes:
            if self.opcolor in str(game.board[move[y]][move[x]]):
                print(self.color, self.opcolor)
                validMoves.append(move)
        if game.board[yT][x] == '   ':
            validMoves.append([yT,cor[x]])
        return validMoves
        pass

class king(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "K"
        self.desig = self.color + self.type + str(self.num)
    def validMove(self, x, y):
        pass
    def movement(self):
        pass

class queen(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "Q"
        self.desig = self.color + self.type + str(self.num)
    def movement(self):
        pass

class bishop(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "B"
        self.desig = self.color + self.type + str(self.num)
    def movement(self):
        pass

class rook(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "R"
        self.desig = self.color + self.type + str(self.num)
    def movement(self):
        pass

class knight(piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "N"
        self.desig = self.color + self.type + str(self.num)
        
    def movement(self,game):
        coords = self.checkPos(game)
        y = coords[0]
        x = coords[1]
        for p in [1,2]:
            if p == 2:
                i = 1
            else:
                i = 2
            
            if (y + p < 8) or (x + i < 8):
                spot = game.board[y+p][x+i]
                pass
            elif (y - p > 0) or (x - i > 0):
                spot = game.board[y+p][x+i]
                pass
            pass
        pass



p1 = []

black = ["bK","bQ"]
white = ["wK","wQ"]

black[0] = king("b")
black[1] = queen("b")
white[0] = king("w")
white[1] = queen("w")
    
print(black[0].color)
for p in range(8):
    black.append(pawn("b", p))
    white.append(pawn("w", p))
for p in range(2):
    black.append(bishop("b", p))
    black.append(knight("b", p))
    black.append(rook("b", p))
    white.append(bishop("w", p))
    white.append(knight("w", p))
    white.append(rook("w", p))
game = Chess(black,white)
Cor = {}
game.setBoard()
game.showBoard()
#game.allPieceCoords()
game.showBoard()
print(game.players[0][3].movement(game))
