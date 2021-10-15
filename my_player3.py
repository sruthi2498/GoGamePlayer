from copy import deepcopy
import math
import random
# import time

# from jsonUtil import writeJson,readJson
from boardUtil import calculateUtilityOfBoard, valid_place_check, remove_died_pieces,isBoardEmpty,compare_board


PLAYER_BLACK = 1
PLAYER_WHITE = 2


class MyPlayer():
    def __init__(self, piece_type):
        self.piece_type = piece_type
        self.minmax_depth = 3
        self.boardSize = 5

    def checkMinMaxLeafNode(self,depth,current_piece,consecutive_pass_count,moveCount):
        if moveCount>25 or depth>=self.minmax_depth or consecutive_pass_count==2 :
            return True
        return False

    def generateMoves(self,board):
        moves=[]
        for i in range(0,self.boardSize):
            for j in range(0,self.boardSize):
                if board[i][j]==0:
                    moves.append([i,j])
        #moves.append([-1,-1])
        random.shuffle(moves)
        return moves

    def MinValue(self,previous_board,board,depth,current_piece,consecutive_pass_count, alpha, beta,moveCount):
        #print("MinValue depth = ",depth)
        action = "PASS"
        if  self.checkMinMaxLeafNode(depth,current_piece,consecutive_pass_count,moveCount):
            return calculateUtilityOfBoard(board,self.piece_type),action
        next_piece = 2 if current_piece == 1 else 1
        v = math.inf
        
        test_board = deepcopy(board)
        for i,j in self.generateMoves(board):
            if valid_place_check(test_board,i, j, current_piece, test_check = True):
                old = test_board[i][j]
                test_board[i][j] = current_piece

                test_board_2 = deepcopy(test_board)
                dead_pieces,test_board_2 = remove_died_pieces(test_board_2,3-self.piece_type)

                if not(dead_pieces and compare_board(previous_board,test_board_2)):
                
                    currVal,_ = self.MaxValue(previous_board,test_board_2,depth+1,next_piece,0,alpha, beta,moveCount+1)
                    #print("MinValue ",i,j,currVal)
                    if currVal<v:
                        v = currVal
                        action = [i,j]

                    test_board[i][j]=old
                    if v<=alpha:
                        return v,action
                    beta = min(beta,v)

        # action : pass
        # noActionVal,_ = self.MaxValue(test_board,depth+1,next_piece,consecutive_pass_count+1,alpha, beta)
        # if noActionVal < v:
        #     #print("MinValue : v = ",v," noActionVal = ",noActionVal)
        #     v = noActionVal
        #     action = "PASS"
        return v,action


    def MaxValue(self,previous_board,board,depth,current_piece,consecutive_pass_count,alpha, beta,moveCount):
        #print("MaxValue depth = ",depth)
        action = "PASS"
        if self.checkMinMaxLeafNode(depth,current_piece,consecutive_pass_count,moveCount):
            return calculateUtilityOfBoard(board,self.piece_type),action
        next_piece = 2 if current_piece == 1 else 1
        v = -math.inf
        
        test_board = deepcopy(board)
    
        for i,j in self.generateMoves(board):
            if valid_place_check(test_board,i, j, current_piece, test_check = True):
                old = test_board[i][j]
                test_board[i][j] = current_piece
                test_board_2 = deepcopy(test_board)
                dead_pieces,test_board_2 = remove_died_pieces(test_board_2,3-self.piece_type)

                if not(dead_pieces and compare_board(previous_board,test_board_2)):
                    currval,_ = self.MinValue(previous_board,test_board_2,depth+1,next_piece,0,alpha, beta,moveCount+1)
                    if currval>v:
                        #print("MaxValue ",i,j,currval)
                        v = currval
                        action = [i,j]

                    test_board[i][j]= old
                    if v>=beta:
                        #print("MaxValue : Returning v = ",v," at ",i,j)
                        return v,action
                    alpha = max(alpha,v)
            

        # action : pass
        # noActionVal,_ = self.MinValue(test_board,depth+1,next_piece,consecutive_pass_count+1,alpha, beta)
        # if noActionVal > v :
        #     #print("MaxValue : v = ",v," noActionVal = ",noActionVal)
        #     v = noActionVal
        #     action = "PASS"
        
        return v,action

    def AlphaBetaSearch(self,previous_board,board, moveCount):
        _,action = self.MaxValue(previous_board,board,0,self.piece_type,0,-math.inf,math.inf,moveCount)
        return action



    def get_next_move(self,previous_board, board, moveCount):
        if self.piece_type==1 and moveCount==1:
            return [1,1]
        action = self.AlphaBetaSearch(previous_board,board, moveCount)
        print(action)
        return action


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



def resetMoveCount():
    with open("movecount.txt","w") as f:
        f.write("0")

def getMoveCount():
    count = 0
    with open("movecount.txt") as f:
        count = int(f.read())
    return count

def updateMoveCount(count):
    print("move count = ",count)
    with open("movecount.txt","w") as f:
        f.write(str(count))
    f.close()



if __name__ == "__main__":
    # start = time.time()
    N = 5   
    piece_type, previous_board, board = readInput(N)
    player = MyPlayer( piece_type)
    if(isBoardEmpty(previous_board)):
        resetMoveCount()
        moveCount = 1 if isBoardEmpty(board) else 2
        player.minmax_depth = 3
    else:
        moveCount = getMoveCount()+2
        if moveCount > 10 :
            player.minmax_depth = 4
        elif moveCount > 20:
            player.minmax_depth = 5
    updateMoveCount(moveCount)

    
    #print(board)
    action = player.get_next_move(previous_board,board,moveCount)
    writeOutput(action)
    # dump_data()
    # print("Time =",time.time()-start)

    # piece_type =2 
    # board=[[0,0,0,0,0],[1,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    # visualize_board(board)
    # player.get_next_move(board)
    #print(valid_place_check(board,2, 2, 1, test_check = True))
    #print("Liberty for 3,1",check_liberty_exists(board,3,1,2,[]))
    
    #
    # print(check_liberty_exists(board,0,1,1,[]))
    # print(find_died_pieces(board,))