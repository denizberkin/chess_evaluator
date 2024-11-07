""" 
scripts to check current game state for now? 
read a pgn file and print game
"""

import os
from typing import *
import logging

import numpy as np
import chess
import chess.pgn as pgn
from tqdm import tqdm

from utils.serialize import BoardState


# Configure logging
logging.basicConfig(filename='game_processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# score from white's perspective
RESULTS = {
    "1-0": 1,
    "0-1": -1,
    "1/2-1/2": 0,
}


def read_games_from_folder(folder: str) -> List[pgn.Game]:
    """ Read all PGNs from a folder """
    games = []
    for fn in os.listdir(folder):
        if fn.endswith(".pgn"):
            file_path = os.path.join(folder, fn)
            print(file_path)
            games.extend(read_games_from_pgn(file_path)) # extend to all games
    return games


def read_games_from_pgn(fn: str) -> List[pgn.Game]:
    """ ??? """
    # FIXME: idk what happened, stopped working, will check?
    games = []
    file_size = os.path.getsize(fn)
    pgn_bytes = open(fn)
    
    with open(fn) as pgn_bytes:
        pbar = tqdm(total=file_size, desc="Reading game file", unit="byte")
        game = pgn.read_game(pgn_bytes)
        while game is not None:
            try:
                logging.DEBUG(f"Loaded game: {game.headers["White"]} vs {game.headers["Black"]}")
                games.append(game)
            except Exception as e:
                logging.error(f"Error reading game: {e}")
                break
            
            # update pbar
            pbar.update(pgn_bytes.tell() - pbar.n)
            game = pgn.read_game(pgn_bytes)
            
        pbar.close()
    
    logging.info(f"Loaded {len(games)} games from {fn}\n")
    return games


def configure_dataset(games: List[pgn.Game], 
                      limit=None
                      ) -> Tuple[np.ndarray, np.ndarray]:
    """ 
    dataset generation for train, val, test
    Q: Should I use yield as this may get heavy with a large set?
    Returns: 
        - X: list of board states
        - y: list of scores
    """
    X, Y = [], []
    num_samples = 0
    
    for game in tqdm(games, desc="Processing games", unit="game"):
        result = game.headers["Result"] if "Result" in game.headers else None
        if result not in RESULTS:
            logging.warning(f"Skipping game due to invalid result: {game.headers}")
            continue  # skip game if result is broken somehow
        
        y = RESULTS[result]  # score from white's perspective
        board = chess.Board()
        
        for move in game.mainline_moves():
            # unfortunately, even the bad moves of the winning side are appointed as positive
            board.push(move)
            x = BoardState(board).board2np()
            X.append(x)
            Y.append(y)
            
            if limit is not None and len(Y) >= limit:
                logging.info(f"Reached limit of {limit} samples, stopping!")
                return np.array(X), np.array(Y)
            
            num_samples += 1
    
    return np.array(X), np.array(Y)
            

if __name__ == "__main__":
    folder = "data"
    fn = "data/Nakamura.pgn"
    
    games = read_games_from_pgn(fn)  # this is only for one pgn, for folder
    # games = read_games_from_folder(folder)
    
    X, Y = configure_dataset(games)
    
    np.savez("processed/pgnmentor.npz", X=X, Y=Y)
    
    