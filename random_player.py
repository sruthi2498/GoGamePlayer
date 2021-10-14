import random
from host import GO

class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, board, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(5):
            for j in range(5):
                if board[i][j]==0:
                    possible_placements.append((i,j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
    	res = "PASS"
    else:
	    res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    # go = GO(N)
    # go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(board,piece_type)
    writeOutput(action)