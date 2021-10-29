from my_player3 import *

N = 5   
piece_type=1
player = MyPlayer( piece_type)

previous_board=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,0,0],[0,0,1,0,0]]
board=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,0,0],[0,2,1,0,0]]
displayBoard(board)

moveCount = 10
player.get_next_move(previous_board,board,moveCount)

# moves,_ = generateAllMoves(board,piece_type,10)
# print(moves)
# moves = sortMovesByDeadOpponents(board,moves,piece_type)
# print(moves)
# dp,tb = getResultBoard(board,[4,4],1)
# displayBoard(tb)
# print(calculateUtilityOfBoard(board,tb,1,10))

# board1=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,1,0],[0,2,1,0,0]]
# displayBoard(board1)
# print(calculateUtilityOfBoard(board,board1,piece_type,10,True))
# board2=[[0,0,0,0,0],[0,1,1,2,0],[0,1,2,2,0],[0,1,2,0,0],[0,2,1,1,0]]
# displayBoard(board2)
# print(calculateUtilityOfBoard(board,board2,piece_type,10,True))