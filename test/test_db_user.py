import logging
import logging.config
import random
import json
from dotenv import load_dotenv
import sys
import os
import pathlib
import random
# sys.path.append(os.path.join(
#     str(pathlib.Path(os.path.abspath(__file__)).parent.parent), "data"))
sys.path.append(str(pathlib.Path(os.path.abspath(__file__)).parent.parent))
from data.db_config import DbConfig # pylint: disable=F0401
from data.db_user import DbUser # pylint: disable=F0401
import pytest

@pytest.fixture()
def db_val():
    print("setup")
    db_config_instance = DbConfig()
    db_user = DbUser(db_config_instance)
    yield db_user
    print("teardown")


class TestDbUser():
    """pytest discovers all tests following its Conventions for Python test discovery, 
    so it finds both test_ prefixed functions. There is no need to subclass anything, 
    but make sure to prefix your class with Test otherwise the class will be skipped. 
    We can simply run the module by passing its filename:
    """

    def test_create_user(self,db_val):
        pytest.email_id = f"test_{random.randint(10000,300000)}" 

        obj = {"first_name" : "Oce_test", "last_name": "Tudose", "email_address" : pytest.email_id, "skill_level":4}
        
        res = db_val.post_user(obj)
        pytest.user_id = res[0]
        assert res[1]==None


    def test_get_user_by_email(self,db_val):
        res = db_val.get_user(email=pytest.email_id)
        assert res[1]==None
        assert pytest.user_id == res[0][0]["id"]

    def test_get_user_by_id(self,db_val):
        res = db_val.get_user(pytest.user_id)
        assert res[1]==None
        assert pytest.user_id == res[0][0]["id"]


    def test_update_user(self,db_val):
        # update user
        obj = {"first_name" : "Oceanna3", "last_name": "Tudose",  "skill_level":random.randint(1,4)}
        res= db_val.put_user(obj,pytest.user_id)
        assert res[1]==None


    def test_deactivate_user(self,db_val):
        obj = {"is_deprecated" : True}
        res= db_val.put_user(obj,pytest.user_id)
        assert res[1]==None
        res = db_val.get_user(pytest.user_id)
        assert res[1]==None
        assert res[0][0]["is_deprecated"]==True


    



