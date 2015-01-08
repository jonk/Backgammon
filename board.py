from players import Players

class Board(object):
    "The board that holds the backgammon game!"
    def __init__(self):
        self.whiteDict = {}
        self.blackDict = {}
        self.initializeBoard(self.whiteDict)
        self.initializeBoard(self.blackDict)
        # print self.whiteDict
        # print self.blackDict
        # print Players.White
        # print Players.Black


    def initializeBoard(self, board):
        i = -1
        while i < 25:
            board[i] = 0
            i += 1
        # board[0] = 2
        # board[11] = 5
        # board[16] = 3
        # board[18] = 5
        # board[-1] = 2
        board[20] = 1
        board[21] = 1

    def movePiece(self, move, player):
        for i in range(len(move)):
            if player == Players.Black:
                self.blackDict[move[i][0]] -= 1
                self.blackDict[move[i][1]] += 1
                if self.whiteDict[move[i][1]] == 1:
                    self.whiteDict[move[i][1]] = 0
                    self.whiteDict[-1] += 1
            elif player == Players.White:
                self.whiteDict[move[i][0]] -= 1
                self.whiteDict[move[i][1]] += 1
                if self.blackDict[move[i][1]] == 1:
                    self.blackDict[move[i][1]] = 0
                    self.blackDict[-1] += 1
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


    def newValidMoves(self, player, rolls):
        total_moves = []

        #Handle Doubles
        if rolls[0] == rolls[1]:
            rolls.extend(rolls)


        #Handle Jail Cell
        if player == Players.White and self.whiteDict[-1] > 0:

            if self.whiteDict[-1] == 1:
                for roll in rolls:
                #One indexed backgammon so 24
                    if self.blackDict[24 - roll] < 2:
                        new_rolls = list(rolls)
                        new_rolls.remove(roll)
                        new_moves = []
                        new_moves.append((-1, roll - 1))
                        self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)

            else:
                num_in_jail = self.whiteDict[-1]
                new_rolls = list(rolls)
                new_moves = []
                while (len(new_rolls) > 0 and num_in_jail > 0):
                    temp = new_rolls[0]
                    new_rolls.remove(new_rolls[0])
                    if self.blackDict[24 - temp] < 2:
                        new_moves.append((-1, temp - 1))
                        num_in_jail -= 1
                if num_in_jail == 0 and len(new_rolls) > 0:
                    self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)
                else:
                    total_moves.append(new_moves)

        elif player == Players.Black and self.blackDict[-1] > 0:

            if self.blackDict[-1] == 1:
                for roll in rolls:
                #One indexed backgammon so 24
                    if self.whiteDict[24 - roll] < 2:
                        new_rolls = list(rolls)
                        new_rolls.remove(roll)
                        new_moves = []
                        new_moves.append((-1, roll - 1))
                        self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)

            else:
                num_in_jail = self.blackDict[-1]
                new_rolls = list(rolls)
                new_moves = []
                while (len(new_rolls) > 0 and num_in_jail > 0):
                    temp = new_rolls[0]
                    new_rolls.remove(new_rolls[0])
                    if self.whiteDict[24 - temp] < 2:
                        new_moves.append((-1, temp - 1))
                        num_in_jail -= 1
                if num_in_jail == 0 and len(new_rolls) > 0:
                    self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)
                else:
                    total_moves.append(new_moves)


        else:
            self.newValidMovesHelper(player, rolls, [], total_moves)

        return total_moves


    # Made outer function to call this as helper
    def newValidMovesHelper(self, player, rolls, cur_moves, total_moves):
        if player == Players.White:
            dict = self.whiteDict
            opponent_dict = self.blackDict
        else:
            dict = self.blackDict
            opponent_dict = self.whiteDict

        for roll in rolls:
            for pos in range(25 - roll):
                new_dict = dict.copy()
                new_opponent_dict = opponent_dict.copy()
                for move in cur_moves:
                    new_dict[move[0]] -= 1
                    new_dict[move[1]] += 1
                if new_dict[pos] > 0 and new_opponent_dict[23 - (pos + roll)] < 2 and (pos + roll) < 24:
                    if len(rolls) == 1:
                        new_moves = list(cur_moves)
                        new_moves.append((pos, pos + roll))
                        if new_moves not in total_moves:
                            total_moves.append(new_moves)
                    else:
                        new_rolls = list(rolls)
                        new_rolls.remove(roll)
                        new_moves = list(cur_moves)
                        new_moves.append((pos, pos + roll))
                        self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)
                elif self.isEating(new_dict) and pos + roll >= 24:
                    while new_dict[pos] == 0 and self.helper(new_dict, roll):
                        pos += 1
                        if pos > 23:
                            break
                    if new_dict[pos] > 0:
                        move = (pos, 24)
                        if len(rolls) == 1:
                            new_moves = list(cur_moves)
                            new_moves.append(move)
                            if new_moves not in total_moves:
                                total_moves.append(new_moves)
                        else:
                            new_rolls = list(rolls)
                            new_rolls.remove(roll)
                            new_moves = list(cur_moves)
                            new_moves.append(move)
                            self.newValidMovesHelper(player, new_rolls, new_moves, total_moves)               
            if len(rolls) == 1:
                return

    def isEating(self, dict):
        i = -1
        while i < 18:
            if dict[i] > 0:
                return False
            i += 1
        return True

    def helper(self, dict, roll):
        for i in range(18, 24 - roll):
            if dict[i] > 0:
                return False
        return True

    #Piece position, checks whether a piece is at the given position
    def pP(self, col, row):
        whiteCol = self.whiteDict[col]
        blackCol = self.blackDict[23 - col]
        if whiteCol > blackCol:
            if (whiteCol > 5 and row == 0):
                return whiteCol
            elif (whiteCol > row and whiteCol <= 5):
                return "+"
        else:
            if (blackCol > 5 and row == 0):
                return blackCol
            elif (blackCol > row and blackCol <= 5):
                return "#"
        return " "

    #Helper to print the board
    def printBoard(self):
        print       "+ - - - - - - || - - - - - - +\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |    + == White\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |    # == Black\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
                    "|-------------||-------------|\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
              "| {} {} {} {} {} {} || {} {} {} {} {} {} |\n" \
                    "+ - - - - - - || - - - - - - +".format(
            self.pP(12, 0), self.pP(13, 0), self.pP(14, 0), self.pP(15, 0), self.pP(16, 0), self.pP(17, 0), self.pP(18, 0), self.pP(19, 0), self.pP(20, 0), self.pP(21, 0), self.pP(22, 0), self.pP(23, 0),
            self.pP(12, 1), self.pP(13, 1), self.pP(14, 1), self.pP(15, 1), self.pP(16, 1), self.pP(17, 1), self.pP(18, 1), self.pP(19, 1), self.pP(20, 1), self.pP(21, 1), self.pP(22, 1), self.pP(23, 1),
            self.pP(12, 2), self.pP(13, 2), self.pP(14, 2), self.pP(15, 2), self.pP(16, 2), self.pP(17, 2), self.pP(18, 2), self.pP(19, 2), self.pP(20, 2), self.pP(21, 2), self.pP(22, 2), self.pP(23, 2),
            self.pP(12, 3), self.pP(13, 3), self.pP(14, 3), self.pP(15, 3), self.pP(16, 3), self.pP(17, 3), self.pP(18, 3), self.pP(19, 3), self.pP(20, 3), self.pP(21, 3), self.pP(22, 3), self.pP(23, 3),
            self.pP(12, 4), self.pP(13, 4), self.pP(14, 4), self.pP(15, 4), self.pP(16, 4), self.pP(17, 4), self.pP(18, 4), self.pP(19, 4), self.pP(20, 4), self.pP(21, 4), self.pP(22, 4), self.pP(23, 4), 
            self.pP(11, 4), self.pP(10, 4), self.pP(9, 4), self.pP(8, 4), self.pP(7, 4), self.pP(6, 4),self.pP(5, 4), self.pP(4, 4), self.pP(3, 4), self.pP(2, 4), self.pP(1, 4), self.pP(0, 4),
            self.pP(11, 3), self.pP(10, 3), self.pP(9, 3), self.pP(8, 3), self.pP(7, 3), self.pP(6, 3),self.pP(5, 3), self.pP(4, 3), self.pP(3, 3), self.pP(2, 3), self.pP(1, 3), self.pP(0, 3),
            self.pP(11, 2), self.pP(10, 2), self.pP(9, 2), self.pP(8, 2), self.pP(7, 2), self.pP(6, 2),self.pP(5, 2), self.pP(4, 2), self.pP(3, 2), self.pP(2, 2), self.pP(1, 2), self.pP(0, 2),
            self.pP(11, 1), self.pP(10, 1), self.pP(9, 1), self.pP(8, 1), self.pP(7, 1), self.pP(6, 1),self.pP(5, 1), self.pP(4, 1), self.pP(3, 1), self.pP(2, 1), self.pP(1, 1), self.pP(0, 1),
            self.pP(11, 0), self.pP(10, 0), self.pP(9, 0), self.pP(8, 0), self.pP(7, 0), self.pP(6, 0),self.pP(5, 0), self.pP(4, 0), self.pP(3, 0), self.pP(2, 0), self.pP(1, 0), self.pP(0, 0))


        
