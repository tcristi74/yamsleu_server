from .db_executer import DbExecuter
from .db_config import DbConfig
from .db_helper import DbHelper
import logging
import json
from typing import Tuple,List
query_response = Tuple[object, str]
users_list = List[int]
from calc.tabel import Tabel

class DbGame(DbExecuter):
    def __init__(self,db_config_instance :DbConfig):
        super().__init__(db_config_instance)

    def new_game(self,game_name:str = None,game_comments:str =None) ->query_response :
        logging.debug(f"Create new game")

        query = f"insert into public.games(game_name,game_comments) values ( %s,%s) RETURNING id;"
        res = super().execute(query,(game_name ,game_comments ),True)
        return res


    def update_game(self,dic_fields: any,game_id:int ) ->query_response :
        logging.debug(f"Update Game id:{game_id}")

        res = super().update_records("games",dic_fields,{"id":game_id})
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

    def get_games(self, conditions)->query_response:
        
        conditions_names = list(conditions.keys())
        use_plays_filters = len([a for a in conditions_names if a[:5]=="plays"])>0
            

        logging.debug("get games for filters")
        columns_game =["games.id","games.game_name","games.started_at","games.ended_at","games.status","games.game_comments","games.winner_id", "games.score" \
            ,"games.modified_at","games.created_at","games.marked_for_deletion" ] 
        columns_as_string = ",".join(map(str,columns_game))
        query = f"select distinct {columns_as_string} from games"
        if use_plays_filters:
            query+=" left outer join plays on games.id=plays.game_id"

        conditions_names = list(conditions.keys())
        if conditions is not None and len(conditions)>0:
            query+=" where " + \
                    " and ".join(map(str, [conditions_names[i]+ " = %s " for i in range(len(conditions_names))]))
        args_list=list(conditions.values())
        recordset= super().get_query(query,tuple(args_list))
        if (recordset[1]!=None):
            return recordset
        if len(recordset[0])==0:
            return ({},None)
        rows= DbHelper.recordset_to_dic(columns_game,recordset[0])
        return (rows,None)


    def update_play(self,dic_fields: any,game_id:int , user_id:int) ->query_response :
        logging.debug(f"update play for gameid:{game_id}, user_id:{user_id}")

        res = super().update_records("plays",dic_fields,{"game_id":game_id, "user_id": user_id})
        return res

    def get_game_plays(self,game_id:int) ->query_response :
        logging.debug(f"get all plays belonging to game :{game_id}")
        columns_game =["g.id","g.game_name","g.started_at","g.ended_at","g.status","g.game_comments","g.winner_id", "g.score" \
            ,"g.modified_at as game_modified_at","g.created_at as game_created_at","g.marked_for_deletion" ] 
        columns_plays = ["game_id","user_id","current_position","current_score","play_table","comments","p.modified_at","p.created_at"]
        
        columns_as_string = ",".join(map(str,columns_game+columns_plays))
        query = f"select {columns_as_string} \
            from games g inner join plays p on g.id=p.game_id \
            where g.id = %s"
        recordset= super().get_query(query,(game_id,))
        if (recordset[1]!=None):
            return recordset
        if len(recordset[0])==0:
            return ({},None)

        t = recordset[0][:1]
        row_game= DbHelper.recordset_to_dic(columns_game,t)
        rows_play = DbHelper.recordset_to_dic(columns_plays,recordset[0],len(columns_game))
        row_game[0]["plays"]=rows_play
        
        return (row_game[0],None)



    def update_tabel(self,column_name:str,row_name:str, game_id:int,user_id:int, value:int,recalculate:bool=False) ->query_response :
        logging.debug(f"update play for gameid:{game_id}, user_id:{user_id}")
        tabel_search = "{{tabel,{0},{1}}}".format(column_name,row_name)
        query = "update plays set play_table = jsonb_set(play_table,%s,'%s') where game_id=%s and user_id=%s"
        args = (tabel_search, value,game_id,user_id)
        res = super().execute(query,args)
        return res
    

    # def __create_tabel_as_array(self):
    #     play = {"tabel":[],"history":[]}
    #     columns = ["I1","I2","I3","I4","P","I","L1","L2","L3","L4","D","T","K","Y"]
    #     rows = ["1","2","3","4","5","6","T","F","q","Q","K","Y","m","M"]
    #     for i in range(len(columns)):
    #         obj = {"id":i+1,"column_name":columns[i]}         
    #         for r in rows:
    #             obj[r]=None
    #         play["tabel"].append(obj)
    #     return play

    def __create_tabel(self):
        play = {"tabel":{},"history":[]}
        columns = ["I1","I2","I3","I4","P","I","L1","L2","L3","L4","D","T","K","Y"]
        rows = ["1","2","3","4","5","6","T","F","q","Q","K","Y","m","M","Total"]
        for c in columns:
            play["tabel"][c]={}    
            for r in rows:
                play["tabel"][c][r]=None
        return play



        




