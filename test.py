from my_player3 import *

N = 5   
piece_type, previous_board, board = readInput(N)
player = MyPlayer( piece_type)
# if(isBoardEmpty(previous_board)):
#     resetMoveCount()
#     moveCount = 1 if isBoardEmpty(board) else 2
# else:
#     moveCount = getMoveCount()+2

# action = player.get_next_move(previous_board,board,moveCount)
# writeOutput(action)

previous_board=[[0,0,0,0,0],[2,1,1,1,1],[2,1,2,1,2],[2,1,2,1,0],[0,2,2,1,0]]
board=[[0,2,0,0,0],[2,1,1,1,1],[2,1,2,1,2],[2,1,2,1,0],[0,2,2,1,0]]
displayBoard(board)
piece_type=1
moveCount = 10
player.get_next_move(previous_board,board,moveCount)

#dp,tb = player.get_result_state(board,[4,0],1)
#print(tb)
#displayBoard(tb)