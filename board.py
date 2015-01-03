from players import Players

class Board(object):
    "The board that holds the backgammon game!"
    def __init__(self):
        self.whiteDict = {}
        self.blackDict = {}
        self.initializeBoard(self.whiteDict)
        self.initializeBoard(self.blackDict)
        print self.whiteDict
        print self.blackDict
        print Players.White
        print Players.Black


    def initializeBoard(self, board):
        i = -1
        while i < 25:
            board[i] = 0
            i += 1
        board[0] = 2
        board[11] = 5
        board[16] = 3
        board[18] = 5

    def movePiece(self, start, dest, player):
        if player == Players.Black:
            self.blackDict[start] -= 1
            self.blackDict[dest] += 1
        elif player == Players.White:
            self.whiteDict[start] -= 1
            self.whiteDict[dest] += 1
        else:
            print "u r a dumdum"

    def isGameOver(self):
        if self.whiteDict[24] == 15:
            return Players.White
        elif self.blackDict[24] == 15:
            return Players.Black
        return 0

    def hasPieceInJail(self, player):
        if player == Players.Black and self.blackDict[-1] > 0:
            return True
        elif player == Players.White and self.whiteDict[-1] > 0:
            return True
        return False


    # DOUBLES AND JAIL
    def validMoves(self, player, roll):
        moves = []
        if player == Players.White:
            dict = self.whiteDict
            opponentDict = self.blackDict
        else:
            dict = self.blackDict
            opponentDict = self.whiteDict
        for i in range(24 - roll[0]):
            temp_dict = dict.copy()
            temp_opponent_dict = opponentDict.copy()
            if temp_dict[i] > 0:
                # if there isn't more than 2 on the black side
                if (23 - (i + roll[0])) in temp_opponent_dict and temp_opponent_dict[23 - (i + roll[0])] < 2:
                    temp_dict[i] -= 1
                    temp_dict[(i + roll[0])] += 1
                    if temp_opponent_dict[23 - (i + roll[0])] == 1:                        
                        temp_opponent_dict[23 - (i + roll[0])] -= 1
                        temp_opponent_dict[-1] += 1
                    for j in range(24 - roll[1]):                   
                        if temp_dict[j] > 0 and temp_opponent_dict[23 - (j + roll[1])] < 2:
                            if ((j, j + roll[1]), (i, i + roll[0])) not in moves and ((i, i + roll[0]), (j, j + roll[1])) not in moves:
                                moves.append(((i, i + roll[0]), (j, j + roll[1])))

        for i in range(24 - roll[1]):
            temp_dict = dict.copy()
            temp_opponent_dict = opponentDict.copy()
            if temp_dict[i] > 0:
                # if there isn't more than 2 on the black side
                if (23 - (i + roll[1])) in temp_opponent_dict and temp_opponent_dict[23 - (i + roll[1])] < 2:
                    temp_dict[i] -= 1
                    temp_dict[(i + roll[1])] += 1
                    if temp_opponent_dict[23 - (i + roll[1])] == 1:                        
                        temp_opponent_dict[23 - (i + roll[1])] -= 1
                        temp_opponent_dict[-1] += 1
                    for j in range(24 - roll[0]):                    
                        if temp_dict[j] > 0 and temp_opponent_dict[23 - (j + roll[0])] < 2:
                            if ((j, j + roll[0]), (i, i + roll[1])) not in moves and ((i, i + roll[1]), (j, j + roll[0])) not in moves:
                                moves.append(((i, i + roll[1]), (j, j + roll[0])))
        return moves


        
b = Board()
print b.validMoves(Players.Black, (5, 5))
