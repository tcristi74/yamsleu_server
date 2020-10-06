from .db_executer import DbExecuter
from .db_config import DbConfig
from .db_helper import DbHelper
import logging
from typing import Tuple
query_response = Tuple[object, str]

class DbUser(DbExecuter):
    def __init__(self,db_config_instance :DbConfig):
        super().__init__(db_config_instance)
    
    def get_user(self,userid:int=None, email:str=None) ->query_response :
        logging.debug(f"get user for userid={userid} or email:{email}")
        columns = ["id", "first_name", "last_name","email_address","skill_level","is_deprecated"]
        columns_as_string = ",".join(map(str,columns))
        query = f"select {columns_as_string} from users where {'id' if userid !=None else 'email_address'}= %s"
        val_tuple = tuple([(userid if userid !=None else email)])
        recordset = super().get_query(query,val_tuple)
        if (recordset[1]!=None):
            return recordset
        rows = DbHelper.recordset_to_dic(columns,recordset[0])

        return (rows,None)


    def get_users(self):
        logging.debug("get users")

    def post_user(self, user_obj:object) -> query_response:
        logging.debug("post user")
        #obj = {"first_name" : "Oceanna", "last_name": "Tudose", "email_address" : "oceanna@abs.com", "skill_level":4}
        if "skill_level" not in user_obj:
            user_obj["skill_level"]=1
        res = super().insert_one_record(user_obj,"users","id")
        #logging.debug(f"port result:{res}")
        return res

    def put_user(self, user_obj:object, id :int) -> query_response:
        """
        Example 
        update users 
         	set last_name = 'tudose1',first_name='cristi1', skill_level=3,email_address='demo@ww.com'
         	where id=2
        """
        if id is None:
            id=user_obj['id']
        logging.debug(f"put user ID: {id}")


        set_conditions= DbHelper.dic_to_string(user_obj, ["id"])
        changes=", ".join(map(str,set_conditions))
    
        query = f"update users set {changes} where id={id}"

        res = super().execute(query,False)
        #logging.debug(f"port result:{res}")
        return res

