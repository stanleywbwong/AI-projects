from engines import Engine
from copy import deepcopy
#import time

class StudentEngine(Engine):
    """ Game engine that you should you as skeleton code for your 
    implementation. """

    alpha_beta = False

    final_depth = 2 #set depth of algorithm searches
    # CLASS ATTRIBUTES for Part VI
    #total_nodes = 0 #counter for total nodes generated
    #num_calls = 0 #counter for number of times each algorithm is called
    #all_nodes = [] #list of all previously explored nodes
    #duplicate_nodes = 0 #counter for number of duplicated nodes explored
    #num_expansions = 0.001 #counter for number of nodes expanded
    #prev_time = time.clock() #time reset at the start of each function call to calculate time elapsed

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Wrapper function that chooses either vanilla minimax or 
        alpha-beta. """
        f = self.get_ab_minimax_move if self.alpha_beta else self.get_minimax_move
        return f(board, color, move_num, time_remaining, time_opponent)

    def get_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):

        # PART VI METRICS #
        #self.num_calls += 1
        #time_elapsed = time.clock() - self.prev_time
        #prev_time = time.clock()
        #print(time_elapsed/self.num_calls)

        #arguments for initial function call
        depth = 0 
        original_moves = board.get_legal_moves(color)
        
        def max_value(board, depth, first_move): #maximizing player
            
            # PART VI METRICS #
            #if depth == 0:
            #    self.num_expansions += 1

            moves = board.get_legal_moves(color)
            max_utility = -99999
            outcomes = [] #list of utilities at each leaf node and the first move by max player leading to that leaf

            if depth == self.final_depth or moves == []:
                return self.evaluate_board(board, color), first_move #evaluate board state, return utility and first move by max player leading to that state

            if depth == 0: #recurse through to leaf level, special case for depth 0 to pass first_move argument through the tree
                for move in moves:
                    newBoard = deepcopy(board)
                    newBoard.execute_move(move, color)
                    utility, best_move = (min_value(newBoard, depth + 1, move))
                    # PART VI METRICS #
                    #self.total_nodes += 1
                    #if move in self.all_nodes:
                    #    self.duplicate_nodes += 1
                    #else:
                    #    self.all_nodes.append(move)
                    outcomes.append((utility, best_move))
                    
            else: #recurse through to leaf level for all depths, passing the first_move along since depth = 0
                for move in moves:
                    newBoard = deepcopy(board)
                    newBoard.execute_move(move, color)
                    utility, best_move = (min_value(newBoard, depth + 1, first_move))
                    # PART VI METRICS #
                    #self.total_nodes += 1
                    #if move in self.all_nodes:
                    ##    self.duplicate_nodes += 1
                    #else:
                    #    self.all_nodes.append(move)
                    outcomes.append((utility, best_move))

            for outcome in outcomes: #iterate through outcome list to search for max utility and return the first_move that would lead to that leaf
                if outcome[0] > max_utility:
                    max_utility = outcome[0]
                    best_move = outcome[1]

            return max_utility, best_move

        def min_value(board, depth, first_move): #minimizing opponent player, same as maximizing but with -color instead of color

            moves = board.get_legal_moves(-color)
            #self.num_expansions += 1
            min_utility = 99999
            outcomes = []

            if depth == self.final_depth or moves == []:
                return self.evaluate_board(board, -color), first_move

            for move in moves:
                newBoard = deepcopy(board)
                newBoard.execute_move(move, -color)
                utility, best_move = (max_value(newBoard, depth + 1, first_move))
                # PART VI METRICS #
                #self.total_nodes += 1
                #if move in self.all_nodes:
                #    self.duplicate_nodes += 1
                #else:
                #    self.all_nodes.append(move)
                outcomes.append((utility, best_move))

            for outcome in outcomes:
                if outcome[0] < min_utility:
                    min_utility = outcome[0]
                    best_move = outcome[1]

            return min_utility, best_move

        # PART VI METRICS #
        #board.display(0)
        #print(self.total_nodes/self.num_calls)
        #print(self.duplicate_nodes/self.num_calls)
        #print(self.total_nodes/self.num_expansions)
        return (max_value(board, depth, None))[1]

    def get_ab_minimax_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        
        # PART VI METRICS #
        #self.num_calls += 1
        #time_elapsed = time.clock() - self.prev_time
        #prev_time = time.clock()
        #print(time_elapsed/self.num_calls)
        depth = 0
        original_moves = board.get_legal_moves(color)
        
        def max_value(board, depth, alpha, beta, first_move): #same as minimax with extra alpha/beta arguments
            
            moves = board.get_legal_moves(color)
            #if depth == 0:
            #    self.num_expansions += 1
            max_utility = -99999
            outcomes = []

            if depth == self.final_depth or moves == []:
                return self.evaluate_board(board, color), first_move

            if depth == 0:
                for move in moves:
                    newBoard = deepcopy(board)
                    newBoard.execute_move(move, color)
                    utility, best_move = (min_value(newBoard, depth + 1, alpha, beta, move)) #pass alpha/beta through to next level
                    alpha = max(alpha, utility) #update alpha
                    if beta <= alpha: #pruning condition
                        break
                    # PART VI METRICS #
                    #self.total_nodes += 1
                    #if move in self.all_nodes:
                    #    self.duplicate_nodes += 1
                    #else:
                    #    self.all_nodes.append(move)
                    outcomes.append((utility, best_move))
                    
            else:
                for move in moves:
                    newBoard = deepcopy(board)
                    newBoard.execute_move(move, color)
                    utility, best_move = (min_value(newBoard, depth + 1, alpha, beta, first_move))
                    alpha = max(alpha, utility)
                    if beta <= alpha:
                        break
                    # PART VI METRICS #
                    #self.total_nodes += 1
                    #if move in self.all_nodes:
                    #    self.duplicate_nodes += 1
                    #else:
                    #    self.all_nodes.append(move)
                    outcomes.append((utility, best_move))

            for outcome in outcomes:
                if outcome[0] > max_utility:
                    max_utility = outcome[0]
                    best_move = outcome[1]

            return max_utility, best_move

        def min_value(board, depth, alpha, beta, first_move): #same as minimax with extra alpha/beta arguments

            moves = board.get_legal_moves(-color)
            #self.num_expansions += 1
            min_utility = 99999
            outcomes = []

            if depth == self.final_depth or moves == []:
                return self.evaluate_board(board, -color), first_move

            for move in moves:
                newBoard = deepcopy(board)
                newBoard.execute_move(move, -color)
                utility, best_move = (max_value(newBoard, depth + 1, alpha, beta, first_move))
                beta = min(beta, utility) #update beta
                if beta <= alpha: #pruning condition
                    break
                # PART VI MEtRICS #
                #self.total_nodes += 1
                #if move in self.all_nodes:
                #    self.duplicate_nodes += 1
                #else:
                #    self.all_nodes.append(move)
                outcomes.append((utility, best_move))

            for outcome in outcomes:
                if outcome[0] < min_utility:
                    min_utility = outcome[0]
                    best_move = outcome[1]

            return min_utility, best_move

        # PART VI METRICS #
        #board.display(0)
        #print(self.total_nodes/self.num_calls)
        #print(self.duplicate_nodes/self.num_calls)
        #print(self.total_nodes/self.num_expansions)
        return (max_value(board, depth, -99999, 99999, None))[1]

    def _get_cost(self, board, color, move):
        """
        Return the difference in number of pieces after the given move 
        is executed.
        """
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op

    def evaluate_board(self, board, color): #evaluation function for static board
                mySquares = board.get_squares(color)
                oppSquares = board.get_squares(-color)

                #CORNER HEURISTIC - return greater positive value for more corner pieces compared to opponent
                corners = [(0,0), (0,7), (7,0), (7,7)]
                cornerCount = 0
                
                for square in mySquares:
                    if square in corners:
                        cornerCount += 1

                for square in oppSquares:
                    if square in corners:
                        cornerCount -= 1

                #EDGE HEURISTIC - return greater postiive value for more edge pieces compared to opponent
                edges = []
                for i in range(8):
                    for j in range(8):
                        if i == 0 or i == 7 or j == 0 or j == 7:
                            edges.append((i,j))
                edgeCount = 0

                for square in mySquares:
                    if square in edges:
                        edgeCount += 1

                for square in oppSquares:
                    if square in edges:
                        edgeCount -= 1

                #CORNER LEAD HEURISTIC - return greater negative value for player pieces on spots that can lead to a capture at the corner by opponent
                cornerleads = [(1,1), (1,6), (6,1), (6,6), (0,1), (1,0), (0,6), (1,7), (6,7), (7,6), (6,0), (7,1)]
                cornerleadCount = 0
                for square in mySquares:
                    if square in cornerleads:
                        cornerleadCount += 1

                for square in oppSquares:
                    if square in cornerleads:
                        cornerleadCount -= 1

                #add all heuristics with set weights and return as utility of a certain board
                squareDiff = 1*(len(mySquares) - len(oppSquares))
                cornerHeuristic = 4*cornerCount
                edgeHeuristic = 2*edgeCount
                cornerleadHeuristic = -3*cornerleadCount
                mobilityHeuristic = 1*(len(board.get_legal_moves(color)) - len(board.get_legal_moves(-color)))
                utility = squareDiff + cornerHeuristic + edgeHeuristic + cornerleadHeuristic + mobilityHeuristic

                return utility
        
engine = StudentEngine
