from agent import Agent
import sys
import string

class UserAgent(Agent):
    """User agent that takes moves from the command line"""

    "Takes in format of 'start dest' ex. 1 3 12 15, on roll (2, 3)"
    def choose_move(self, validMoves=()): 
        sys.stdout.write("Input move:\n> ")
        line = sys.stdin.readline()
        moves = string.split(line)
        result = []
        i = 0
        while i < len(moves) - 1:
            move = (int(moves[i]), int(moves[i+1]))
            result.append(move)
            i += 2
        return result