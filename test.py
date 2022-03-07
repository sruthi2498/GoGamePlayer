from my_player3 import *

N = 5   
piece_type=2
player = MyPlayer( piece_type)

previous_board=[[0,1,0,0,0],[0,2,2,1,0],[0,2,2,2,1],[1,1,2,2,1],[0,1,0,0,0]]
board=[[0,1,0,0,0],[0,2,2,1,0],[0,2,2,2,1],[1,1,2,2,1],[0,1,0,0,0]]
displayBoard(board)

moveCount = 10
player.get_next_move(previous_board,board,moveCount)

# moves,_ = generateAllMoves(board,piece_type,10)
# print(moves)
# moves = sortMxovesByDeadOpponents(board,moves,piece_type)
# print(moves)
dp,tb = getResultBoard(board,[1,4],piece_type)
displayBoard(tb)
print(calculateUtilityOfBoard(board,tb,piece_type,10,True))

dp,tb2 = getResultBoard(board,[0,2],piece_type)
displayBoard(tb2)
print(calculateUtilityOfBoard(board,tb2,piece_type,10,True))

# MyPlayer( 2).get_next_move(board,tb,moveCount+1)

# board1=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,1,0],[0,2,1,0,0]]
# displayBoard(board1)
# print(calculateUtilityOfBoard(board,board1,piece_type,10,True))
# board2=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,0,0],[0,2,1,1,0]]
# displayBoard(board2)
# print(calculateUtilityOfBoard(board,board2,piece_type,10,True))