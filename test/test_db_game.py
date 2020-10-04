import logging
import logging.config
import random
import json
from dotenv import load_dotenv
import sys
import os
import pathlib
# sys.path.append(os.path.join(
#     str(pathlib.Path(os.path.abspath(__file__)).parent.parent), "data"))
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from data.db_config import DbConfig
from data.db_game import DbGame
import datetime



def create_game():

    db_play = DbGame(db_config_instance)
    res = db_play.new_game("game test 18")
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def update_game(update_dic, game_id):

    db_play = DbGame(db_config_instance)
    res = db_play.update_game(update_dic,game_id)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def create_play(game_id):

    db_play = DbGame(db_config_instance)
    res = db_play.new_play([10,11],game_id)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def update_play(update_dic,game_id,user_id):
    db_play = DbGame(db_config_instance)
    res = db_play.update_play(update_dic,game_id,user_id)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def update_tabel(game_id,user_id):
    db_play = DbGame(db_config_instance)
    res = db_play.update_tabel("I1","3",game_id,user_id,9)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def get_plays(game_id):
    db_play = DbGame(db_config_instance)
    res = db_play.get_game_plays(game_id)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def get_games_with_filters(filters):
    db_play = DbGame(db_config_instance)
    res = db_play.get_games(filters)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]


if __name__ == "__main__":
    # logging.config.fileConfig('logging.conf')
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")
    db_config_instance = DbConfig()
    email_id = f"test_{random.randint(10000,300000)}"

    new_game_id = create_game()
    ret = create_play(new_game_id)
    player_id = ret[0]
    update_dic = {
                  "started_at": datetime.datetime.now(),
                  "status": "started",
                  "game_comments": "this is a test",
                  "winner_id": player_id,
                  "score": 1000
                  }
    ret = update_game(update_dic, new_game_id)

    update_dic = {
                  "started_at": datetime.datetime.now(),
                  "status": "started",
                  "game_comments": "this is a test",
                  "winner_id": None,
                  "score": 1000
                  }
    ret = update_game(update_dic, new_game_id)


    update_dic = {
                  "current_position": -1,
                  "comments": "this is a test",
                  "current_score": 1000
                  }
    ret = update_play(update_dic, new_game_id,player_id)

    ret = update_tabel(new_game_id,player_id)

    ret = get_plays(new_game_id)

    ret = get_games_with_filters({
                  "plays.user_id": 11
                  })
    
    ret = get_games_with_filters({
                  "id": 56
                  })




    print(ret)



    



