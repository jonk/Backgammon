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
        board[0] = 2
        board[11] = 5
        board[16] = 3
        board[18] = 5
        board[-1] = 2

    def movePiece(self, start, dest, player):
        if player == Players.Black:
            self.blackDict[start] -= 1
            self.blackDict[dest] += 1
            if self.whiteDict[dest] == 1:
                self.whiteDict[dest] = 0
                self.whiteDict[-1] += 1
        elif player == Players.White:
            self.whiteDict[start] -= 1
            self.whiteDict[dest] += 1
            if self.blackDict[dest] == 1:
                self.blackDict[dest] = 0
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


    #TODO Eating valid moves

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

        print total_moves
        return total_moves


    # MADE outer function to call this as helper

    def newValidMovesHelper(self, player, rolls, cur_moves, total_moves):
        if player == Players.White:
            dict = self.whiteDict
            opponent_dict = self.blackDict
        else:
            dict = self.blackDict
            opponent_dict = self.whiteDict

        for roll in rolls:
            for pos in range(24 - roll):
                new_dict = dict.copy()
                new_opponent_dict = opponent_dict.copy()
                for move in cur_moves:
                    new_dict[move[0]] -= 1
                    new_dict[move[1]] += 1
                if new_dict[pos] > 0 and new_opponent_dict[23 - (pos + roll)] < 2:
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
            if len(rolls) == 1:
                return


b = Board()
b.newValidMoves(Players.White, [5, 5])



        
