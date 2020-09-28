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
from data.db_play import DbPlay


def create_play():

    db_play = DbPlay(db_config_instance)
    res1 = db_play.new_play([1],1)
    return res1




if __name__ == "__main__":
    #logging.config.fileConfig('logging.conf')
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")
    db_config_instance = DbConfig()
    email_id = f"test_{random.randint(10000,300000)}" 

    ret= create_play()
    assert (ret[1]==None),f"error:{ret[1]}"


    



