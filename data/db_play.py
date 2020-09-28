from .db_executer import DbExecuter
from .db_config import DbConfig
from .db_helper import DbHelper
import logging
import json
from typing import Tuple,List
query_response = Tuple[object, str]
users_list = List[int]

class DbPlay(DbExecuter):
    def __init__(self,db_config_instance :DbConfig):
        super().__init__(db_config_instance)
    
    def new_play(self,users:users_list, game_id:int) ->query_response :
        logging.debug(f"Create new play for users ids{ ','.join(map(str,users))}")
        tabel=self.__create_tabel()

        obj = {"game_id" : game_id, "user_id": users[0],"play_table" : json.dumps(tabel)}
        res = super().insert_one_record(obj,"plays")
        #logging.debug(f"port result:{res}")
        return res

    def __create_tabel(self):
        play = {"tabel":[],"history":[]}
        columns = ["I1","I2","I3","I4","P","I","L1","L2","L3","L4","D","T","K","Y"]
        rows = ["1","2","3","4","5","6","T","F","q","Q","K","Y","m","M"]
        for i in range(len(columns)):
            obj = {"id":i+1,"column_name":columns[i]}         
            for r in rows:
                obj[r]=None
            play["tabel"].append(obj)
        return play

        




