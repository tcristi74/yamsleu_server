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


def create_play(game_id):

    db_play = DbGame(db_config_instance)
    res = db_play.new_play([10,11],game_id)
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]

def create_game():

    db_play = DbGame(db_config_instance)
    res = db_play.new_game("game test' 1")
    assert (res[1]==None),f"error:{res[1]}"
    return res[0]



if __name__ == "__main__":
    #logging.config.fileConfig('logging.conf')
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")
    db_config_instance = DbConfig()
    email_id = f"test_{random.randint(10000,300000)}" 

    new_game_id = create_game()
    ret= create_play(new_game_id)
    print (ret)



    



