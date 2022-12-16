import chess as ch
import random as rd

class AI_Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.AI_engine_driver(None, 1)

    def evalFunct(self):
        counters = 0
        for i in range(64):
            counters += self.sqaureResPoints(ch.SQUARES[i])
        counters += self.mateOpportunity() + self.opening() + 0.001 * rd.random()
        return counters


    def mateOpportunity(self):
        if(self.board.legal_moves.count() == 0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0

    def opening(self):
        if (self.board.fullmove_number < 10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    # takes square and returns Hans Berliner residents points
    # of the specific square
    # pawn 1
    # knight 3.2
    # bishop 3.33
    # rook 5.1
    # queen 8.8
    def sqaureResPoints(self, square):
        pieceValue = 0
        if (self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 1
        if (self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 3.2
        if (self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 3.33
        if (self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 5.1
        if (self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 8.8
        
        if(self.board.color_at(square) != self.color):
            return -pieceValue
        else:
            return pieceValue

    def AI_engine_driver(self, candidate, depth):
        if (depth == self.maxDepth or self.board.legal_moves.count()==0):
            return self.evalFunct()
        else:
            moveList = list(self.board.legal_moves)
            newCandidate = None
        
            if (depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            for i in moveList:
                self.board.push(i)
                value = self.AI_engine_driver(newCandidate, depth+1)
                # min max wo AB pruning
                #if maximizing (AI)
                if(value > newCandidate and depth % 2 != 0):
                    newCandidate = value
                    if(depth == 1):
                        move = i
                # if minimizing (HUMAN)
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value
                
                #AB pruning 
                # AI
                if(candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                # HUMAN
                elif(candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                # undo last move
                self.board.pop()
        if(depth >1):
            # value of the node in the tree
            return newCandidate
        else:
            return move
