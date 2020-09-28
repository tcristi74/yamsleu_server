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
from data.db_user import DbUser


def create_user():
    # insert test 
    obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
    db_user = DbUser(db_config_instance)
    res1 = db_user.post_user(obj)
    return res1



def get_user():
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
    email_id = f"test_{random.randint(10000,300000)}" 

    ret= create_user()
    #assert (ret[1]==None),f"error:{ret[1]}"
    ret_dic = get_user()
    assert (ret_dic[1]==None),f"error:{ret_dic[1]}"
    user_id =ret_dic[0][0]["id"]
    assert (user_id>0),"problem with userid"+ json.dumps(ret_dic[0][0])
    
    ret = update_user()
    assert (ret[1]==None),f"error:{ret[1]}"
    print ("db_users = done")

    



