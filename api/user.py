from flask_restful import Resource,abort,reqparse
from flask import jsonify,request,Response,make_response
import json 
from data.db_user import DbUser
from data.db_config import DbConfig

# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class User(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 

  
    def get(self,user_id): 
        db_user = DbUser(DbConfig())
        res_val_db=db_user.get_user(userid=user_id)
        response = make_response(jsonify({"response":res_val_db}),200 )
        return response

    def delete(self,user_id): 

        obj = {"is_deprecated" : True}
        db_user = DbUser(DbConfig())
        res= db_user.put_user(obj,user_id)
        is_success = res[1] is None

        response = make_response(jsonify({"error":res[1]}),204 if is_success else 400 )
        return response


    def put(self,user_id): 
        req_body = request.get_json()     # status code

            
        need_fetch = False if "fetch" not in request.values else request.values["fetch"].lower()=="true"
        db_user = DbUser(DbConfig())
        res_val_db=db_user.put_user(req_body,user_id)
        is_success = res_val_db[1] is None

        res_body = {"success":is_success}
        if not is_success:
            res_body["error"] = res_val_db[1]
        
        if need_fetch and  is_success:
            return self.get(user_id)

        response = make_response(jsonify(res_body),204 if is_success else 400)
        #response.headers['X-Parachutes'] = 'parachutes are cool'  
        return response

