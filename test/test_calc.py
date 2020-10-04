import logging
import logging.config
import random
import json
from dotenv import load_dotenv
import sys
import os
import pathlib
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from calc.tabel import Tabel




def calculate_tabel():
    # insert test 
    obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
    calc = Tabel()
    calc

def recalculate_tabel():
    # insert test 
    obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
    db_user = DbUser(db_config_instance)
    res1 = db_user.post_user(obj)
    return res1


def verify_tabel():
    db_user = DbUser(db_config_instance)
    res = db_user.get_user(email=email_id)
    return res


def update_user():
    # update user
    obj = {"first_name" : "Oceanna3", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
    db_user = DbUser(db_config_instance)
    return db_user.put_user(obj,user_id)


def deactivate_user():
    return True



if __name__ == "__main__":
    #logging.config.fileConfig('logging.conf')
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")
    db_config_instance = DbConfig()


    



