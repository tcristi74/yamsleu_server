from flask_restful import Resource,abort,reqparse
from flask import jsonify,request,Response,make_response
import json 
from data.db_game import DbGame
from data.db_config import DbConfig

# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class GameUser(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
  
    def patch(self,game_id,user_id): 
        data = request.get_json() 
        if "column_name" not in data or "row_name" not in data or "value" not in data:
            return make_response(jsonify({"error":"invalid payload (column_name,row_name and value properties are mandatory"}),400)

        db_play = DbGame(DbConfig())
        res = db_play.update_tabel(data["column_name"],data["row_name"],game_id,user_id,data["value"])
        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        else:
            return make_response(jsonify(res),204)

    

    def put(self,game_id,user_id): 
        data = request.get_json() 
        db_play = DbGame(DbConfig())  
        res = db_play.update_play(data,game_id,user_id)

        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        else:
            return make_response(jsonify(res),204)



class Game(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
  
    def get(self,game_id): 
        """this get the game inclusing the plays and the tabels 
        """
        db_play = DbGame(DbConfig())
        res = db_play.get_game_plays(game_id)
        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        else:
            return make_response(jsonify(res),200)

    def put(self,game_id): 
        data = request.get_json() 

        db_play = DbGame(DbConfig())  
        res = db_play.update_game(data,game_id)
        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        else:
            return make_response(jsonify(res),204)

    # def put(self,game_id,user_id): 
    #     data = request.get_json() 

    #     db_play = DbGame(DbConfig())  
    #     res = db_play.update_game(data,game_id)
    #     if res[1] is not None:
    #         return make_response(jsonify({"error":res[1]}),400)
    #     else:
    #         return make_response(jsonify(res),204)


class Games(Resource):

    def patch(self): 
        """The filters are in the body
        """
        data = request.get_json()
        db_play = DbGame(DbConfig())
        res = db_play.get_games(data)
        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        return make_response(jsonify(res),200)
        

    # Corresponds to POST request 
    def post(self): 
        """body fata would lokk like this 
        {"game_name": "this is new game Oct00", "comment": "this is a comment" ,"users" : [{{user_id}},{{user_id2}}]}

        """
        data = request.get_json()   
        if data is None or "game_name" not in data:
            return  make_response(jsonify({"error": "payload is missing or doesn not have a 'game_name' properti"}),400)
        if "users" not in data or not isinstance(data["users"], list) or len(data["users"])==0:
            return  make_response(jsonify({"error": "'users' array property from payload id missing or not properly setup"}),400)

        db_play = DbGame(DbConfig())
        res = db_play.new_game(game_name=data["game_name"],game_comments=None if "comment" not in data else data["comment"])
        if res[1] is not None:
            return make_response(jsonify({"error":res[1]}),400)
        game_id = int(res[0])
        if game_id>0:
            res = db_play.new_play(data["users"],game_id)
            if res[1] is not None:
                return make_response(jsonify({"error":res[1]}),400)
            
            return make_response(jsonify({"game_id":game_id,"users":res[0]}),201)
        else:
            return make_response(jsonify({"error":"game not created"}),400)


