import logging
import logging.config
import random

from dotenv import load_dotenv
import sys
import os
import pathlib
# sys.path.append(os.path.join(
#     str(pathlib.Path(os.path.abspath(__file__)).parent.parent), "data"))
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from data.db_executer import DbExecuter
from data.db_config import DbConfig
from data.db_user import DbUser


def insert_one_record():
    # insert test 
    obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
    db = DbExecuter(db_config_instance)
    res1 = db.insert_one_record(obj,"users")
    if res1[1]!=None:
        return {"sucess":False, "message":res1[1]}
    res2 = db.get_query("select id from public.users where email_address= %s",tuple([email_id]))
    return res2[0][0][0]


def get_query():

    db = DbExecuter(db_config_instance)
    #dbuser = DbUser(db_config_instance)
    res = db.get_query("select * from public.users where id= %s",tuple([user_id]))
    return res


def execute():
    db = DbExecuter(db_config_instance)
    #dbuser = DbUser(db_config_instance)
    res = db.execute("delete from public.users where id= %s",tuple([user_id]))
    return res




if __name__ == "__main__":
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")
    db_config_instance = DbConfig()
    email_id = f"test_{random.randint(10000,300000)}" 

    user_id = insert_one_record()
    assert (user_id>0),"user has not been created"

    ret =  get_query()
    assert (ret[1]==None),f"error:{ret[1]}"

    ret = execute()
    assert (ret[1]==None),f"error:{ret[1]}"

    print ("db_executer = done")

    
    



