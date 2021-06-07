from sqlite3.dbapi2 import Timestamp
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "21cxorcxlyiwautslytprkgmq" # your Spotify username 
TOKEN = "BQCeVyKxQRmEsDq4yqVJZvepPbZjCmOgVP1yRs5fKvRkmHBKYe1LsdKAjgLzHm5QfA8WJYCYvgYdKje01BmzHhkCy6wbhAh3lsu89t7trDWqwAtVylmzfmZGLT_1m2By8dkOS4NacbRu4EoLQfUY-dIdVlue_LTYs3_UyQjv" # your Spotify API token

if __name__ == '__main__':
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000


    r = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)
    print(r)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    print(song_df)