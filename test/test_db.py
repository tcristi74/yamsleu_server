import logging
import logging.config

from dotenv import load_dotenv
import sys
import os
import pathlib
sys.path.append(os.path.join(
    str(pathlib.Path(os.path.abspath(__file__)).parent.parent), "data"))
from db_executer import DbExecuter
from db_config import DbConfig
from db_user import DbUser



if __name__ == "__main__":
    #logging.config.fileConfig('logging.conf')
    logging.basicConfig(filename='info.log', level=logging.INFO)
    logging.getLogger(__name__)
    load_dotenv()

    logging.debug("Start")

    db_config_instance = DbConfig()
    db = DbExecuter(db_config_instance)
    #dbuser = DbUser(db_config_instance)
    res = db.get_query("select * from public.users",
                 None, fetch_results=True)

    # # insert test 
    # obj = {"first_name" : "Oceanna", "last_name": "Tudose", "email_address" : "oceanna@abs.com", "skill_level":4}
    # res = db.insert_one_record(obj,"users")

    # update user
    obj = {"first_name" : "Oceanna3", "last_name": "Tudose", "email_address" : "oceannaww@abs.com", "skill_level":4}
    db_user = DbUser(db_config_instance)
    db_user.put_user(obj,6)

