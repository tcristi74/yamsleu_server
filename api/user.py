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

  
    def get(self,name): 
        response = make_response(jsonify({"name":name}),200 )
        return response
        # if (name!='cristi'):
        #     return jsonify({'message': f'get {name} user'})
        # else: 
        #     abort(404, message=json.dumps({'message':"user doesn't exit"}))

    def put(self,user_id): 
        req_body = request.get_json()     # status code

        # parser = reqparse.RequestParser()
        # args = parser.parse_args()
        
        # path_args = request.view_args
        # if 'user_id' not in path_args:
        #     response = make_response(jsonify({"error": "invalid path. userid need to be passed"}),400)
        #     return response 
        # check for fetch parameter
        
        #if "fetch" in request.values:
            

        db_user = DbUser(DbConfig())
        res_val_db=db_user.put_user(req_body,user_id)

        res_body = {"success": res_val_db[0]}
        if not res_val_db[0]:
            res_body["error"] = res_val_db[1]
        
        need_fetch = False if "fetch" not in request.values else request.values["fetch"].lower()=="true"
        if need_fetch and  res_val_db[0]:
            return self.get(req_body["first_name"])
        else:
            response = make_response(jsonify(res_body),200 if res_val_db[0] else 400)
            response.headers['X-Parachutes'] = 'parachutes are cool'  
            return response

