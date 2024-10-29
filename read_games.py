""" 
scripts to check current game state for now? 
read a pgn file and print game
"""

import os
from typing import *

import numpy as np
import chess
import chess.pgn as pgn


# score from white's perspective
RESULTS = {
    "1-0": 1,
    "0-1": -1,
    "1/2-1/2": 0,
}


def read_games_from_pgn(fn: str) -> List[pgn.Game]:
    """ pgn.read_game reads one game per call!"""
    games = []
    pgn_bytes = open(fn)
    while True:
        try:
            game = pgn.read_game(pgn_bytes)
            if game is None:
                break  # EOF
        except Exception as e:
            print(e)  # some error with file?
            break
        games.append(game)
    
    return games


def configure_dataset(games: List[pgn.Game], 
                      limit=None
                      ) -> Tuple[np.ndarray, np.ndarray]:
    """ 
    dataset for train, val, test
    Returns: 
        - X: list of board states
        - y: list of scores
    """
    X, Y = [], []
    num_samples = 0
    
    for game in games:
        result = game.headers["Result"] if "Result" in game.headers else None
        if result not in RESULTS:
            continue  # skip game if result is broken somehow
        
        y = RESULTS[result]  # score from white's perspective
        board = chess.Board()
        
        for move in game.mainline_moves():
            board.push(move)
            # board2np here
            # TODO: append to X

            # unfortunately, even the bad moves of the winning side 
            # are appointed as positive
            Y.append(y)
            
            if limit is not None and len(Y) >= limit:
                return np.array(X), np.array(Y)
            
            num_samples += 1
    
    return np.array(X), np.array(Y)
            


if __name__ == "__main__":
    fn = "data/one_game.pgn"
    games = read_games_from_pgn(fn)  # each % 2 is metadata, game pair
    for game in games:
        print([(k, v) for k, v in game.headers.items()])  # either -> "1-0", "0-1", "1/2-1/2"
    
    board = chess.Board()  # o(n)
    # print main moves of the game w/format
    for i, move in enumerate(game.mainline_moves()):
        board.push(move)
        print(f"State {i}.\n{board}")
        # print each state, kind of prettified
    
    
    