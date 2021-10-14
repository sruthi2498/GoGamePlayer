from copy import deepcopy
# from jsonUtil import readJson, writeJson,WriterTask
import time

boardSize =5

PLAYER_BLACK = 1
PLAYER_WHITE = 2


def encode_state(state):
    return ''.join([str(state[i][j]) for i in range(boardSize) for j in range(boardSize)])

def get_neighbour_positions(i,j):
    neighbors = []
    if i > 0: neighbors.append((i-1, j))
    if i < boardSize - 1: neighbors.append((i+1, j))
    if j > 0: neighbors.append((i, j-1))
    if j < boardSize - 1: neighbors.append((i, j+1))
    return neighbors

def get_edge_counts(board,board_encoded,my_piece):
    opponent_piece_type = 2 if my_piece==1 else 1
    myTotalCount = 0
    opponentCount=0
    n = len(board)
    i=0
    for j in range(n):
        if board[i][j] == my_piece:
            myTotalCount+=1
        elif board[i][j] == opponent_piece_type:
            opponentCount+=1
    j=0
    for i in range(1,n):
        if board[i][j] == my_piece:
            myTotalCount+=1
        elif board[i][j] == opponent_piece_type:
            opponentCount+=1
    i=n-1
    for j in range(1,n):
        if board[i][j] == my_piece:
            myTotalCount+=1
        elif board[i][j] == opponent_piece_type:
            opponentCount+=1
    j=n-1
    for i in range(1,n-1):
        if board[i][j] == my_piece:
            myTotalCount+=1
        elif board[i][j] == opponent_piece_type:
            opponentCount+=1
    
    return myTotalCount,opponentCount

def get_counts(board,board_encoded,my_piece):
    opponent_piece_type = 2 if my_piece==1 else 1
    myTotalCount = 0
    opponentCount=0
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == my_piece:
                myTotalCount+=1
            elif board[i][j] == opponent_piece_type:
                opponentCount+=1
    return myTotalCount,opponentCount
    
def get_total_first_order_liberty_count(board,locs,piece):
    totalLiberty = 0
    marked=[]
    for i,j in locs:
        neighbs = get_neighbour_positions(i,j)
        for k,l in neighbs:
            if board[k][l]==0:
                neighb_string = str(k)+"_"+str(l)
                if neighb_string not in marked:
                    totalLiberty+=1
                    marked.append(neighb_string)
    return totalLiberty

def get_total_second_order_liberty_count(board,locs,piece):
    locsWithNoEmptyNeighb=[]
    for i,j in locs:
        neighbs = get_neighbour_positions(i,j)
        neighbNotEmptyCount = 0
        for k,l in neighbs:
            if board[k][l]!=0:
                neighbNotEmptyCount+=1
        if  neighbNotEmptyCount == len(neighbs):
            locsWithNoEmptyNeighb.append([i,j])
    
    return get_total_liberty_count(board,locsWithNoEmptyNeighb,piece)
    
def get_total_liberty_count(board,locs,piece):
    totalLiberty = 0
    Visted = []
    for i,j in locs:
        curr = str(i)+"_"+str(j)
        if  curr not in Visted:
            libCount,vis = check_liberty_exists(board,i,j,piece,[])
            #print(i,j,libCount,visited)
            totalLiberty+=libCount
            for v in vis:
                if v!=curr and v not in Visted:
                    totalLiberty+=libCount
                    Visted.append(v)
    return totalLiberty

def get_liberties(board,board_encoded,my_piece):
    opponent_piece_type = 2 if my_piece==1 else 1
    
    my_piece_locs = []
    opponent_piece_locs=[]
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == my_piece:
                my_piece_locs.append([i,j])
            elif board[i][j] == opponent_piece_type:
                opponent_piece_locs.append([i,j])

    
    myFirstOrderLiberty = get_total_first_order_liberty_count(board,my_piece_locs,my_piece)
    oppFirstOrderLiberty = get_total_first_order_liberty_count(board,opponent_piece_locs,opponent_piece_locs)

    mySecondOrderLiberty = get_total_second_order_liberty_count(board,my_piece_locs,my_piece)
    oppSecondOrderLiberty = get_total_second_order_liberty_count(board,opponent_piece_locs,opponent_piece_locs)
        
    return myFirstOrderLiberty,oppFirstOrderLiberty,mySecondOrderLiberty,oppSecondOrderLiberty

def get_dead_count(board,board_encoded,my_piece):
    opponent_piece_type = 2 if my_piece==1 else 1
    myDeadCount = len(find_dead_pieces(board,my_piece))
    oppDeadCount = len(find_dead_pieces(board,opponent_piece_type))
    return myDeadCount,oppDeadCount


# def loadData():
#     data = dataModel.retrieve_data()

def calculateUtilityOfBoard(board, my_piece):

    board_encoded = encode_state(board)
    blackFirstOrderLiberty,whiteFirstOrderLiberty,blackSecondOrderLiberty,whiteSecondOrderLiberty = get_liberties(board,board_encoded,1)

    f1 = blackFirstOrderLiberty - whiteFirstOrderLiberty if my_piece==1 else  whiteFirstOrderLiberty - blackFirstOrderLiberty

    f2 = blackSecondOrderLiberty - whiteSecondOrderLiberty if my_piece==1 else  whiteSecondOrderLiberty - blackSecondOrderLiberty

    # blackEdgeCount,whiteEdgeCount = get_edge_counts(board,board_encoded,1)
    # edgeCountDiff = blackEdgeCount - whiteEdgeCount if my_piece==1 else  whiteEdgeCount - blackEdgeCount  

    blackCount,whiteCount = get_counts(board,board_encoded,1)
    # totalCount = blackCount+whiteCount
    countDiffFactor = 4 if my_piece==1 else 2
    countDiff = blackCount-whiteCount if my_piece==1 else blackCount-whiteCount
    blackScore = blackCount
    whiteScore = whiteCount + 2.5
    

    f5 = blackScore-whiteScore if my_piece==1 else whiteScore-blackScore

    blackEuler,whiteEuler = calculate_euler_number(board,board_encoded,1)
    f4 = blackEuler - whiteEuler if my_piece==1 else  whiteEuler - blackEuler


    utility =  max(f1 + f2  +f5, -4) - (4*f4)  + (countDiffFactor*countDiff)
    
    
    '''
    int score  =  Math.min(Math.max(liberties,-4), 4)  + -4*euler + 5*numOfPieces  + numOnEdge '''
    # if my_piece==1:
    #     utility = min( max(blackFirstOrderLiberty+blackSecondOrderLiberty,-4),4 ) - (4* blackEuler) + (5*blackCount)  
    # else:
    #     utility = min( max(whiteFirstOrderLiberty+whiteSecondOrderLiberty,-4),4 ) - (4* whiteEuler) + (5*whiteCount)
    return  utility

def get_quad_type(board,i,j, piece_type): #quad till (i,j) = (i-1,j-1) (i-1,j) (i,j-1) (i,j)
    one = 0 if i-1 < 0 or j-1 <0 or board[i-1][j-1]!=piece_type else 1
    two = 0 if i-1 < 0 or j <0 or j>=boardSize or board[i-1][j]!=piece_type else 1
    three = 0 if i < 0 or i>=boardSize or j-1 <0  or board[i][j-1]!=piece_type else 1
    four = 0 if i < 0 or i>=boardSize or j<0 or j>=boardSize  or board[i][j]!=piece_type else 1
    sum = one+two+three+four
    if sum==1:
        return "q1"
    elif sum==2 and (\
         (  i-1>=0 and j-1>=0 and board[i-1][j-1]==piece_type and i<boardSize and j<boardSize and  board[i][j]==piece_type ) \
             or\
         ( i<boardSize and  j-1>=0 and  board[i][j-1]==piece_type and i-1>=0 and j<boardSize and board[i-1][j]==piece_type ) ):
        return "qd"
    elif sum==3:
        return "q3"
    return "none"
        
def calculate_quad_counts(board,piece_type):
    quad_dict={"q1":0,"q3":0,"qd":0,"none":0}
    for i in range(0,boardSize+1):
        for j in range(0,boardSize+1):
            quad_dict[get_quad_type(board,i,j,piece_type)]+=1
    return quad_dict

def calculate_euler_number(board,board_encoded,my_piece):
    opponent_piece_type = 2 if my_piece==1 else 1
    quad_dict = calculate_quad_counts(board,my_piece)
    my_euler =  (quad_dict["q1"]-quad_dict["q3"] + (2*quad_dict["qd"]))/4

    quad_dict = calculate_quad_counts(board,opponent_piece_type)
    opp_euler =  (quad_dict["q1"]-quad_dict["q3"] + (2*quad_dict["qd"]))/4
    return my_euler,opp_euler


def check_liberty_exists(board, k,l,piece_type, visited ):
    #print("Liberty check at ",k,l)
    current_pos_string= str(k)+"_"+str(l)
    neighbs = get_neighbour_positions(k,l)
    opponent_piece_type = 2 if piece_type==1 else 1
    opponent_neighbs = 0
    friend_neighbs=[]
    c=0
    for i,j in neighbs :
        if board[i][j]==0:
            c+=1
            #return True,visited
        elif board[i][j]==opponent_piece_type:
            opponent_neighbs+=1
        elif str(i)+"_"+str(j) not in visited:
            friend_neighbs.append([i,j])
    if c:
        return c, visited
    # surrounded by opponents
    if opponent_neighbs == len(neighbs):
        return 0,visited
    visited.append(current_pos_string)
    neigbhsLibertyCount = 0
    neighbsVisited = []
    for i,j in friend_neighbs:
        currLib,neighbVisited = check_liberty_exists(board,i,j,piece_type, visited )
        #print("at neighb ",i,j, "liberty = ",currLib)
        neigbhsLibertyCount = neigbhsLibertyCount + currLib
        neighbsVisited = visited + neighbVisited
        if neigbhsLibertyCount :
            return neigbhsLibertyCount,list(set(neighbsVisited ))

    return neigbhsLibertyCount,list(set(neighbsVisited ))

    
def find_dead_pieces(board, piece_type):
    died_pieces = []
    allVisited = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == piece_type:
                if str(i)+"_"+str(j) in allVisited:
                    died_pieces.append((i,j))
                else:
                    hasLiberty, visited = check_liberty_exists(board,i,j, piece_type,[])
                    if not hasLiberty:
                        allVisited = allVisited + visited
                        died_pieces.append((i,j))
    return died_pieces


def remove_certain_pieces(board, positions):
    for piece in positions:
        board[piece[0]][piece[1]] = 0
    return board


def remove_died_pieces(board, piece_type):
    died_pieces = find_dead_pieces(board,piece_type)
    if not died_pieces: return [],board
    board=remove_certain_pieces(board,died_pieces)
    return died_pieces,board

def compare_board( board1, board2):
    for i in range(boardSize):
        for j in range(boardSize):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def valid_place_check(board, i, j, piece_type, test_check=False):
    
    verbose = True
    if test_check:
        verbose = False

    # Check if the place is in the board range
    if not (i >= 0 and i < len(board)):
        #if verbose:
            #print(('Invalid placement. row should be in the range 1 to {}.').format(len(board) - 1))
        return False
    if not (j >= 0 and j < len(board)):
        #if verbose:
            #print(('Invalid placement. column should be in the range 1 to {}.').format(len(board) - 1))
        return False
    
    # Check if the place already has a piece
    if board[i][j] != 0:
        #if verbose:
            #print('Invalid placement. There is already a chess in this position.')
        return False
    
    # Copy the board for testing
    test_board = deepcopy(board)

    # Check if the place has liberty
    test_board[i][j] = piece_type

    liberty_exists,_ = check_liberty_exists(test_board,i,j,piece_type,[])
    #print("First liberty check : ",liberty_exists)
    if liberty_exists:
        return True

    # If not, remove the died piece s of opponent and check again
    opponent_piece_type = 2 if piece_type==1 else 1
    dead_pieces,test_board = remove_died_pieces(test_board,opponent_piece_type)
    #print(dead_pieces)
    liberty_exists,_ = check_liberty_exists(test_board,i,j,piece_type,[])
    #print("Second liberty check : ",liberty_exists)
    if not liberty_exists:
        if verbose:
            print('Invalid placement. No liberty found in this position.')
        return False

    # Check special case: repeat placement causing the repeat board state (KO rule)
    else:
        if dead_pieces and compare_board(board, test_board):
            if verbose:
                print('Invalid placement. A repeat move not permitted by the KO rule.')
            return False
    return True

def store_move_ordering(board_encoded,piece_type,actions):
    print("Storing move ordering for ",board_encoded)
    

def get_move_ordering(board_encoded,piece_type):
    return []
    # if board_encoded not in data or "m" not in data[board_encoded] or str(piece_type) not in data[board_encoded]["m"]:
    #     return []
    # return data[board_encoded]["m"][str(piece_type)]
        

# def dump_data():
#     task = WriterTask(data, "data.txt")
#     task.start()
#     task.join()
    #writeJson(data,"data.txt")

def visualize_board(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                print(' ', end=' ')
            elif board[i][j] == 1:
                print('X', end=' ')
            else:
                print('O', end=' ')
        print()
    print('-' * len(board) * 2)

def isBoardEmpty(board):
    for i in range(boardSize):
        for j in range(boardSize):
            if board[i][j]!=0:
                return False
    return True
	
if __name__ == "__main__":

    board=[[0,2,1,2,1],[0,2,1,1,1],[0,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0]]
    # print(get_liberties(board,encode_state(board),1))
    # print(check_liberty_exists(board,0,2,1,[]))
    print(calculate_quad_counts(board,1))
    # print(calculate_euler_number(board,1))
    # print(check_liberty_exists(boar
    # d,0,1,1,[]))
    # print(find_died_pieces(board,))