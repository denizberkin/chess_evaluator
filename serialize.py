from typing import *

import chess
import numpy as np

# order stated in chess.Piece.symbol(): capital for white, lowercase for black
BOARD_SIZE = 8

# 0-> empty square, 7 and 14 are for castling
PIECE_ENCODINGS = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
                   "p": 8, "n": 9, "b": 10, "r": 11, "q": 12, "k": 13}


class BoardState:
    def __init__(self, board: chess.Board=None) -> Self:
        self.board = board if board is not None else chess.Board()
        
    def board2np(self) -> np.ndarray:
        if not self.board.is_valid():
            raise ValueError("Invalid board state")
        
        # square board
        current_board = np.zeros(BOARD_SIZE ** 2, dtype=np.int8)
        for i in range(BOARD_SIZE ** 2):
            piece: chess.Piece = self.board.piece_at(i)
            if piece is not None:  # else already defined as 0
                current_board[i] = PIECE_ENCODINGS[piece.symbol()]

        # set castling rights
        current_board[0] = 7 if self.board.has_kingside_castling_rights(chess.WHITE) else 0
        current_board[7] = 7 if self.board.has_queenside_castling_rights(chess.WHITE) else 0
        current_board[56] = 14 if self.board.has_kingside_castling_rights(chess.BLACK) else 0
        current_board[63] = 14 if self.board.has_queenside_castling_rights(chess.BLACK) else 0
            
        # en passant
        if self.board.ep_square is not None:
            current_board[self.board.ep_square] = 15
            
        # XXX: change this block in case I want to implement a different representation, 
        # one hot for different pieces might be the case as alpha zero does use a similar implementation
        
        binary_board = np.zeros((5, 8, 8), dtype=np.int8)  # see readme for shape explanation
        
        # need to reshape the current board to 8x8 before applying binary ops
        current_board = current_board.reshape(8, 8)
        for i in range(4):
            binary_board[i] = (current_board >> i) & 1  # shift right i times, then bitwise AND
        binary_board[4] = (self.board.turn * 1.0) # 1.0 for white, 0.0 for black
        
        # END
        
        return current_board  # 5, 8, 8 np array