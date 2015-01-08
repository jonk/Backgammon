from players import Players
from board import Board
from user_agent import UserAgent
import random
import time

def main():
    game = Game()
    game.start()

class Game(object):
    "The game that will control agents and a board."
    def __init__(self):
        self.gameBoard = Board()
        self.blackPlayer = UserAgent(Players.Black)
        self.whitePlayer = UserAgent(Players.White)

    def start(self):
        cur_player = self.whoGoesFirst()
        while True:
            print "{}'s Turn!".format(cur_player.name)
            rolls = [self.roll(), self.roll()]
            print rolls
            possible_moves = self.gameBoard.newValidMoves(cur_player.num, rolls)
            self.gameBoard.printBoard()
            move = cur_player.choose_move()
            while move not in possible_moves:
                print "Not a valid move! Try Again"
                move = cur_player.choose_move()
            self.gameBoard.movePiece(move, cur_player.num)
            if self.gameBoard.isGameOver():
                print "{} is the Winner!".format(cur_player.name)
                return
            self.gameBoard.printBoard()
            if cur_player.num == Players.White:
                cur_player = self.blackPlayer
            else:
                cur_player = self.whitePlayer
            



    def roll(self):
        return random.randrange(1, 7)

    def whoGoesFirst(self):
        white = self.roll()
        print "White rolls a {}".format(white)
        # time.sleep(1)
        black = self.roll()
        print "Black rolls a {}".format(black)
        # time.sleep(1)
        if white > black:
            print "White goes first!"
            return self.whitePlayer
        elif white == black:
            print "It ended in a tie....Everyone wins!"
            # time.sleep(2)
            print "Rolling again..."
            return self.whoGoesFirst()
        else:
            print "Black goes first!"
            return self.blackPlayer


if __name__ == "__main__":
    main()

