import io
import os
import zipfile

import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


""" See: pgnmentor_player_pgns.csv """
def get_filenames_pgnmentor() -> dict:
    """
    Read from players table in https://pgnmentor.com/files.html.
    Returns: dictionary of player, download link and number of games
    """
    URL = "https://www.pgnmentor.com/"
    ext = "files.html"
        
    response = requests.get(URL + ext)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.body.div.find_all('table')[5]
    pgn_dict = {"player": [], "num_games": [], "download_link": []}
    i = 0
    for row in tables.find_all('tr'):
        i += 1
        cols = row.find_all('td')
        
        if len(cols) == 2:
            player_name, num_games = cols[1].text.split(", ")
            pgn_dict["player"].append(player_name)  # get player name
            pgn_dict["num_games"].append(int(num_games.split(" ")[0]))  # num games as int?
            pgn_dict["download_link"].append(URL + cols[0].a['href'])  # get href link
        
    return pgn_dict
        

def save_to_csv(dict_data: dict, dest: str, fn: str) -> None:
    if not os.path.exists(dest):
        os.makedirs(dest)
    df = pd.DataFrame(dict_data)
    df.to_csv(os.path.join(dest, fn), index=False)
    

def download_pgns_from_csv(csv_path: str, dest: str) -> None:
    """
    Download pgn files from the csv file.
    """
    df = pd.read_csv(csv_path)
    
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    pbar = tqdm(df.iterrows(), total=len(df), desc="Downloading PGNs", ncols=80)  
    for index, row in pbar:
        player, dl, num_games = row["player"], row["download_link"], row["num_games"]
        
        tqdm.write(f"Downloading PGN for {player} ({num_games} games)")
        
        response = requests.get(dl)
        response.raise_for_status() # checking if not 200
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip:
            for zip_info in zip.infolist():
                if zip_info.filename.endswith(".pgn"):
                    zip_info.filename = os.path.basename(zip_info.filename)
                    zip.extract(zip_info, dest)
                    
                    tqdm.write(f"Extracted {zip_info.filename} for {player}")
        
    pbar.close()
    tqdm.write("All downloads completed.")
        
        
if __name__ == "__main__":
    # we can also use https://www.ficsgames.org/download.html to download games which can filter to time, player, gamemode etc. 
    # but i currently did not write a script for that.
    dest = "data"
    fn = "pgnmentor_player_pgns.csv"
    
    # to create your csv, you can pass this if you want -> pgnmentor_player_pgns.csv is available
    filenames_dict = get_filenames_pgnmentor()
    save_to_csv(filenames_dict, dest, fn=fn)
    
    # to download games from csv to dest
    csv_fn = "data/pgnmentor_player_pgns.csv"
    download_pgns_from_csv(csv_fn, dest)