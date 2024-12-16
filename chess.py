##Note: Most commits are for comments, I just copy pasted a lot of it from my VSCode
import random

#Class for Players
class Player():
    def __init__(self, color):
        self.color = color
        self.pieces = [] #List of all of a player's pieces
        self.abr = 'w' if color == 'White' else 'b' #To more easily give designations to pieces
        self.givePieces()
        
    def givePieces(self): #Gives the player's pieces
        self.pieces.append(king(self.abr))
        self.pieces.append(queen(self.abr))
        for p in range(8):
            self.pieces.append(pawn(self.abr, p))
        for p in range(2):
            self.pieces.append(bishop(self.abr, p))
            self.pieces.append(knight(self.abr, p))
            self.pieces.append(rook(self.abr, p))
    
    def make_move(self,game):
        print("ERROR! At class Player()") #Checking for errors

#Human Players
class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.givePieces()
        
    def make_move(self,game):
        while True:
            possibleMoves = []
            piece = str(input(f"\nEnter which {self.color} piece you want to move: "))
            gamePiece = None
            for p in self.pieces:
                if p.desig == piece:
                    gamePiece = p
                    possibleMoves = gamePiece.movement(game)
                    break
            
            if gamePiece in self.pieces and gamePiece.eliminated == False and len(possibleMoves) > 0:
                print("\n\nListing Possible Moves...\n\n"+"\033[4m# :  [y, x] \033[0m")
                for moves in range(len(possibleMoves)):
                    print(moves,": ", possibleMoves[moves])
                z = int(input("\nChoose which move: "))
                game.make_move(possibleMoves[z],gamePiece)
                break
            else:
                print("Choose again.")
        return True

#Random AI Player that chooses a random piece and then chooses a random available move for that piece
class AIPlayerRandom(Player):
    def __init__(self, color):
        super().__init__(color)
        self.givePieces()
    def make_move(self,game):
        while True:
            possiblePieces = []
            possibleMoves = []
            z = 0
            gamePiece = None
            for p in self.pieces:
                if p.eliminated == False: 
                    possiblePieces.append(p)
            if len(possiblePieces) == 0:
                return False #Added to check why there were sometimes 0 possible moves to be
            gamePiece = possiblePieces[random.randint(1,len(possiblePieces))-1]
            possibleMoves = gamePiece.movement(game)
            if gamePiece in self.pieces and gamePiece.eliminated == False and len(possibleMoves) > 0:
                z = random.randint(0,len(possibleMoves))-1
                game.make_move(possibleMoves[z],gamePiece)
                break
        
#Class for the game
class Chess():
    def __init__(self, player1, player2):
        self.board = [['   ' for i in range(8)] for i in range(8)]
        self.pieces = {player1.color:player1.pieces, player2.color:player2.pieces}
        self.p1color = player1.color #Honestly, the self.p1color and self.p2color isn't necessarily needed when I could do self.players[x].color
        self.p2color = player2.color #But, by the time I realized this, I already had put this in like 4 different functions and it was 5AM and it's a bit faster to type out.
        self.players = [player1, player2]
    
    def play(self):
        self.setBoard()
        while True:
            for player in self.players:
                self.showBoard()
                x = player.make_move(game)
                self.checkElims() #Checks if any pieces have been eliminated after every move/turn 
                if x == False:
                    print("Draw")
                    self.showBoard()
                winner = self.checkWin()
                if winner != 'None':
                    if winner == 'b':
                        print("Black Wins")
                    else:
                        print("White Wins!")
                    self.showBoard()
                    return winner
                    
    def checkElims(self): #Checks which pieces are on the board. If it's not on the board, it's marked as eliminated
        for colors in [self.p1color,self.p2color]:
            for pieces in self.pieces[colors]:
                for y in range(8):
                    if pieces.desig not in self.board[y]:
                        pieces.eliminated = True
                    else:
                        pieces.eliminated = False
                        break
        return

    def checkWin(self):
        for colors in [self.p1color,self.p2color]:
            king = self.pieces[colors][0] #King is always the first piece appended to the list.
            if king.eliminated == True:
                return king.opcolor
        return 'None'
    
    def showBoard(self): #Went through several different formats for the board. This ended up being the one that looked the best.
        print('')
        print('   ','  0  ', '  1  ', '  2  ', '  3  ', '  4  ', '  5  ', '  6  ', '  7  ')
        print('')
        for y in range(8):
            #print(y, self.board[y])
            print (y, '', '|',self.board[y][0], '|',self.board[y][1], '|',self.board[y][2], '|',self.board[y][3], '|',self.board[y][4], '|',self.board[y][5], '|',self.board[y][6], '|',self.board[y][7],'|',)
            print('   ',' ---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ')
            
    def allPieceCoords(self): #Function added to bug test
        for a in [self.p1color,self.p2color]:
            for pieces in self.pieces[a]:
                print(pieces.desig, self.Cor[pieces])
            print("-")

    def setBoard(self): #Basically puts all the pieces on the board as well as assigns the coordinates for pieces.
        self.board = [['   ' for i in range(8)] for i in range(8)] #Added to wipe the board clean before putting the pieces on the board. Prevents pieces from spilling over from past games
        self.Cor = {} #Dictionary for the coordinates. 
        for x in range(8):
            self.board[1][x] = 'wP'+str(x)
            self.board[6][x] = 'bP'+str(x)
        for c in ['w','b']:
            if c == 'w':
                y=0
            else:
                y=7
            x = 0
            for p in ['R','N','B']:
                self.board[y][x] = c+p+str(0)
                self.board[y][-(1+x)] = c+p+str(1) # -(1+x) is an equation to get the reflected x coordinate
                x = x+1
            for p in range(2):
                self.board[y][x] =  c+'K'+str(0)
                self.board[y][-(1+x)] = c+'Q'+str(0)
                
        for a in [self.p2color,self.p1color]: #Loop that assigns a piece's coords to a 
            for pieces in self.pieces[a]:
                self.Cor[pieces] = pieces.checkPos(game)
        self.checkElims()

    def make_move(self, coords, piece): #Function to actually makes a move on the board
        currPieceCoords = piece.checkPos(game)
        self.board[coords[0]][coords[1]] = piece.desig #First moves the piece to the spot
        self.board[currPieceCoords[0]][currPieceCoords[1]] = '   ' #Then erases itself from the spot it moved from.

#Class for all the pieces on the board
class Piece():
    def __init__(self, color="w", num=0, eliminated=False, type = "type"):
        self.color = color
        self.eliminated = eliminated
        self.type = type 
        if color == 'b':
            self.opcolor = 'w' #opcolor means opponent's color
        else:
            self.opcolor= 'b'
        self.num = num
        self.desig = type + str(num)
        
    def checkPos(self,game): #Gets a piece's current coordinates.
        self.cor = [0,0]
        self.cor[0] = 100 
        self.cor[1] = 100
        if self.eliminated == False:
            for y in range(8):
                if self.desig in game.board[y]:
                    self.cor[0] = y
                    for x in range(8):
                        if self.desig == game.board[y][x]:
                            self.cor[1] = x
        return self.cor #Coordinates are not in [x, y], they're in [y, x] due to how the board is a nested list
    
    def movement(self):
        print("ERROR!") #Bug Testing

class pawn(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "P" #Overides self.type = "type"
        self.desig = self.color + self.type + str(self.num) #Overrides self.desig. Desig is short for designation. 
        
    def movement(self, game): #Probably the most different/unique movement function from the rest of the other pieces, probably because it was the first one. Also, Override.
        validMoves = [] #Only piece that uses validMoves as a list name
        y = 0 #These variables are mostly so I don't get confused which coordinate I am changing since coords are usually (x, y) and not (y, x)
        x = 1
        c = 0 #The 'c' stands for 'color' since it changes values based on the color
        if self.color == 'w':
            c = -1
        else:
            c = 1
        cor = self.checkPos(game)
        yT = cor[y]-c #The possible Y coordinate it can move to. 
        xT = [cor[x]-1, cor[x]+1] #The possible X coordinates it can move to
        takes = [[yT,xT[0]], [yT,xT[1]]]
        if yT < 8 and y > -1:
            if game.board[yT][cor[x]] == '   ':
                validMoves.append([yT,cor[x]])
        for move in takes:
            if (move[y] > -1 and move[y] < 8) and (move[x] > -1 and move[x] < 8):
                if self.opcolor in str(game.board[move[y]][move[x]]):
                    validMoves.append(move)
        
        return validMoves #returns all valid moves.
        

class king(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "K"
        self.desig = self.color + self.type + str(self.num)
        
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        s=1
        if y+s < 8 and x+s < 8:
            if self.color not in str(game.board[y+s][x+s]):
                availableMoves.append([y+s,x+s])
        if y-s > -1 and x-s > -1:
            if self.color not in str(game.board[y-s][x-s]):
                availableMoves.append([y-s,x-s])
        if x+s < 8 and y-s > -1:
            if self.color not in (game.board[y-s][x+s]):
                availableMoves.append([y-s,x+s])
        if x-s > -1 and y+s < 8:
            if self.color not in str(game.board[y+s][x-s]):
                availableMoves.append([y+s,x-s])
        if y+s < 8:
            if self.color not in str(game.board[y+s][x]):
                availableMoves.append([y+s,x])
        if y-s > -1:
            if self.color not in str(game.board[y-s][x]):
                availableMoves.append([y-s,x])
        if x+s < 8:
            if self.color not in str(game.board[y][x+s]):
                availableMoves.append([y,x+s])       
        if x-s > -1:
            if self.color not in str(game.board[y][x-s]):
                availableMoves.append([y,x-s])
        return availableMoves

class queen(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "Q"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        for s in range(1,7):
            if y+s < 8 and x+s < 8:
                if self.color in str(game.board[y+s][x+s]):
                    break
                if self.opcolor in str(game.board[y+s][x+s]):
                    availableMoves.append([y+s,x+s])
                    break
                if game.board[y+s][x+s] == '   ':
                    availableMoves.append([y+s,x+s])
        for s in range(1,7):
            if y-s > -1 and x-s > -1:
                if self.color in str(game.board[y-s][x-s]):
                    break
                if self.opcolor in str(game.board[y-s][x-s]):
                    availableMoves.append([y-s,x-s])
                    break
                if game.board[y-s][x-s] == '   ':
                    availableMoves.append([y-s,x-s])
        for s in range(1,7):
            if x+s < 8 and y-s > -1:
                if self.color in str(game.board[y-s][x+s]):
                    break
                if self.opcolor in str(game.board[y-s][x+s]):
                    availableMoves.append([y-s,x+s])
                    break
                if game.board[y-s][x+s] == '   ':
                    availableMoves.append([y-s,x+s])
        for s in range(1,7):
            if x-s > -1 and y+s < 8:
                if self.color in str(game.board[y+s][x-s]):
                    break
                if self.opcolor in str(game.board[y+s][x-s]):
                    availableMoves.append([y+s,x-s])
                    break
                if game.board[y+s][x-s] == '   ':
                    availableMoves.append([y+s,x-s])
        for s in range(1,7):
            if y+s < 8:
                if self.color in str(game.board[y+s][x]):
                    break
                if self.opcolor in str(game.board[y+s][x]):
                    availableMoves.append([y+s,x])
                    break
                if game.board[y+s][x] == '   ':
                    availableMoves.append([y+s,x])
        for s in range(1,7):
            if y-s > -1:
                if self.color in str(game.board[y-s][x]):
                    break
                if self.opcolor in str(game.board[y-s][x]):
                    availableMoves.append([y-s,x])
                    break
                if game.board[y-s][x] == '   ':
                    availableMoves.append([y-s,x])
        for s in range(1,7):
            if x+s < 8:
                if self.color in str(game.board[y][x+s]):
                    break
                if self.opcolor in str(game.board[y][x+s]):
                    availableMoves.append([y,x+s])
                    break
                if game.board[y][x+s] == '   ':
                    availableMoves.append([y,x+s])
        for s in range(1,7):
            if x-s > -1:
                if self.color in str(game.board[y][x-s]):
                    break
                if self.opcolor in str(game.board[y][x-s]):
                    availableMoves.append([y,x-s])
                    break
                if game.board[y][x-s] == '   ':
                    
                    availableMoves.append([y,x-s])
        return availableMoves
        
        

class bishop(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "B"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        for s in range(1,7):
            if y+s < 8 and x+s < 8:
                if self.color in str(game.board[y+s][x+s]):
                    break
                if self.opcolor in str(game.board[y+s][x+s]):
                    availableMoves.append([y+s,x+s])
                    break
                if game.board[y+s][x+s] == '   ':
                    availableMoves.append([y+s,x+s])
        for s in range(1,7):
            if y-s > -1 and x-s > -1:
                if self.color in str(game.board[y-s][x-s]):
                    break
                if self.opcolor in str(game.board[y-s][x-s]):
                    availableMoves.append([y-s,x-s])
                    break
                if game.board[y-s][x-s] == '   ':
                    availableMoves.append([y-s,x-s])
        for s in range(1,7):
            if x+s < 8 and y-s > -1:
                if self.color in str(game.board[y-s][x+s]):
                    break
                if self.opcolor in str(game.board[y-s][x+s]):
                    availableMoves.append([y-s,x+s])
                    break
                if game.board[y-s][x+s] == '   ':
                    availableMoves.append([y-s,x+s])
        for s in range(1,7):
            if x-s > -1 and y+s < 8:
                if self.color in str(game.board[y+s][x-s]):
                    break
                if self.opcolor in str(game.board[y+s][x-s]):
                    availableMoves.append([y+s,x-s])
                    break
                if game.board[y+s][x-s] == '   ':
                    availableMoves.append([y+s,x-s])
        return availableMoves

class rook(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "R"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        for s in range(1,7):
            if y+s < 8:
                if self.color in str(game.board[y+s][x]):
                    break
                if self.opcolor in str(game.board[y+s][x]):
                    availableMoves.append([y+s,x])
                    break
                if game.board[y+s][x] == '   ':
                    availableMoves.append([y+s,x])
        for s in range(1,7):
            if y-s > -1:
                if self.color in str(game.board[y-s][x]):
                    break
                if self.opcolor in str(game.board[y-s][x]):
                    availableMoves.append([y-s,x])
                    break
                if game.board[y-s][x] == '   ':
                    availableMoves.append([y-s,x])
        for s in range(1,7):
            if x+s < 8:
                if self.color in str(game.board[y][x+s]):
                    break
                if self.opcolor in str(game.board[y][x+s]):
                    availableMoves.append([y,x+s])
                    break
                if game.board[y][x+s] == '   ':
                    availableMoves.append([y,x+s])
        for s in range(1,7):
            if x-s > -1:
                if self.color in str(game.board[y][x-s]):
                    
                    break
                if self.opcolor in str(game.board[y][x-s]):
                    
                    availableMoves.append([y,x-s])
                    break
                if game.board[y][x-s] == '   ':
                    
                    availableMoves.append([y,x-s])
        return availableMoves

class knight(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "N"
        self.desig = self.color + self.type + str(self.num)
        
    def movement(self,game):
        availableMoves = []
        coords = self.checkPos(game)
        y = coords[0]
        x = coords[1]
        for p in [1,2]:
            if p == 2:
                i = 1
            if p == 1:
                i = 2
            
            if (y + p < 8) and (x + i < 8):
                if self.color not in game.board[y+p][x+i]:
                    availableMoves.append([y+p,x+i])
            if (y - p > -1) and (x - i > -1):
                if self.color not in game.board[y-p][x-i]:
                    availableMoves.append([y-p,x-i])
            if (y + p < 8) and (x - i > -1):
                if self.color not in game.board[y+p][x-i]:
                    availableMoves.append([y+p,x-i])
            if (y - p > -1) and (x + i < 8):
                if self.color not in game.board[y-p][x+i]:
                    availableMoves.append([y-p,x+i])     
        return availableMoves    
        





if __name__ == "__main__": #Main Function
    #playerB = HumanPlayer("Black")
    playerB = AIPlayerRandom("Black")
    #playerW = HumanPlayer("White")
    playerW = AIPlayerRandom("White")
    game = Chess(playerW,playerB)

    print(game.pieces[game.p1color][3].desig)

    bk = 0
    wt = 0

    for x in range(1):
        w = game.play()
        if w == "w":
            wt += 1
        if w == "b":
            bk += 1

    print("Black", bk, "| White", wt)
