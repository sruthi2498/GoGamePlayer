from my_player3 import *

N = 5   
piece_type=1
player = MyPlayer( piece_type)

previous_board=[[0,2,1,1,2],[1,1,1,2,0],[2,1,2,2,2],[2,1,1,1,2],[0,1,1,2,0]]
board=[[0,2,1,1,2],[1,1,1,2,2],[2,1,2,2,2],[2,1,1,1,2],[0,1,1,2,0]]
displayBoard(board)

moveCount = 10
player.get_next_move(previous_board,board,moveCount)

# moves,_ = generateAllMoves(board,piece_type,10)
# print(moves)
# moves = sortMovesByDeadOpponents(board,moves,piece_type)
# print(moves)
dp,tb = getResultBoard(board,[4,4],1)
displayBoard(tb)
print(calculateUtilityOfBoard(board,tb,1,10))

dp,tb2 = getResultBoard(board,[4,0],1)
displayBoard(tb2)
print(calculateUtilityOfBoard(board,tb2,1,10))