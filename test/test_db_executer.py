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
from data.db_executer import DbExecuter # pylint: disable=F0401
from data.db_config import DbConfig # pylint: disable=F0401
import pytest

@pytest.fixture()
def db():
    print("setup")
    db_config_instance = DbConfig()
    db_exec = DbExecuter(db_config_instance)
    yield db_exec
    print("teardown")


class TestDbExecuter():

    def test_nsert_one_record(self,db):
        # insert test 
        email_id = f"test_{random.randint(10000,300000)}" 
        obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : email_id, "skill_level":4}
        res = db.insert_one_record(obj,"users")
        assert res[1]==None
        res = db.get_query("select id from public.users where email_address= %s limit 10",tuple([email_id]))
        assert res[1]==None
        pytest.user_id= res[0][0][0]
        assert pytest.user_id>0


    def test_get_query(self,db):
        res = db.get_query("select * from public.users where id= %s",tuple([pytest.user_id]))
        assert res[1]==None
        assert len(res[0])==1


    def test_execute_query(self,db):
        res = db.execute("delete from public.users where id= %s",tuple([pytest.user_id]))
        return res




# if __name__ == "__main__":
#     logging.basicConfig(filename='info.log', level=logging.INFO)
#     logging.getLogger(__name__)
#     load_dotenv()

#     logging.debug("Start")
#     db_config_instance = DbConfig()
#     email_id = f"test_{random.randint(10000,300000)}" 

#     user_id = insert_one_record()
#     assert (user_id>0),"user has not been created"

#     ret =  get_query()
#     assert (ret[1]==None),f"error:{ret[1]}"

#     ret = execute()
#     assert (ret[1]==None),f"error:{ret[1]}"

#     print ("db_executer = done")

    
    



