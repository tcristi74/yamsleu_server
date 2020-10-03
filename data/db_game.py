from .db_executer import DbExecuter
from .db_config import DbConfig
from .db_helper import DbHelper
import logging
import json
from typing import Tuple,List
query_response = Tuple[object, str]
users_list = List[int]

class DbGame(DbExecuter):
    def __init__(self,db_config_instance :DbConfig):
        super().__init__(db_config_instance)

    def new_game(self,game_name:str = None,game_comments:str =None) ->query_response :
        logging.debug(f"Create new game")

        query = f"insert into public.games(game_name,game_comments) values ( %s,%s) RETURNING id;"
        res = super().execute(query,(game_name ,game_comments ),True)
        return res


    def update_game(self,dic_fields: any,game_id:int ) ->query_response :
        logging.debug(f"Create new game")

        res = super().update_records("games",dic_fields,{"id":game_id})
        if res[1]!=None:
            return res
    
    def new_play(self,users:users_list, game_id:int) ->query_response :
        logging.debug(f"Create new play for users ids{ ','.join(map(str,users))}")
        tabel=self.__create_tabel()
        ids= []
        for user_id in users:
            obj = {"game_id" : game_id, "user_id": user_id,"play_table" : json.dumps(tabel)}
            res = super().insert_one_record(obj,"plays","user_id")
            if res[1]!=None:
                return res
            ids.append(res[0])
        return (ids,None)

        

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



        




