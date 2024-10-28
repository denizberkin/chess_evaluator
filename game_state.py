""" 
scripts to check current game state for now? 
read a pgn file and print game
"""

import chess
import chess.pgn as pgn


# score from white's perspective
score = {
    "1-0": 1.,
    "0-1": -1.,
    "1/2-1/2": 0.,
}


def read_pgn(fn) -> pgn.Game:
    return pgn.read_game(open(fn))




if __name__ == "__main__":
    fn = "data/Nakamura.pgn"
    game = read_pgn(fn)  # each % 2 is metadata, game pair
    
    print(game.headers["Result"])  # either -> "1-0", "0-1", "1/2-1/2"
    
    board = chess.Board()  # o(n)
    # print main moves of the game w/format
    for i, move in enumerate(game.mainline_moves()):
        board.push(move)
        print(f"State {i}.\n{board}")
        # print each state, kind of prettified
    
    
    