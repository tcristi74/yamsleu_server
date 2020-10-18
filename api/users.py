from flask_restful import Resource,abort,reqparse
from flask import jsonify,request,Response,make_response
import json 
from data.db_user import DbUser
from data.db_config import DbConfig

class Users(Resource):

    def get(self):        
        args = request.args
        print (args)
        db_user = DbUser(DbConfig())
        if "filters" in args and args["filters"].lower()=="true":
            data = request.get_json() 
            if "email_address" in data:           
                res_val_db=db_user.get_user(email=data["email_address"])
                
        else:
            limit = 100 if "limit" not in args else int(args["limit"]) 
            offset = 0 if "offset" not in args else int(args["offset"])
            order_by = "first_name" if "orderby" not in args else str(args["orderby"])
            res_val_db=db_user.get_users(order_by,limit,offset)
        if res_val_db[1] is not None:
            return make_response(jsonify({"error":res_val_db[1]}),400 )

        response = make_response(jsonify(res_val_db[0]),200)



        return response

    # Corresponds to POST request 
    def post(self): 
        data = request.get_json()     # status code

        parser = reqparse.RequestParser()
        parser.add_argument('type', help='detail or summary')
        #parser.add_argument('year',type=int, help='detail or summary')
        #args = parser.parse_args()
        # db_user  = 
        
        db_user = DbUser(DbConfig())
        res_val = db_user.post_user(data)
        ret_body = {"id": res_val[0]}
        if not res_val[0]:
            ret_body["error"] = res_val[1]

        response = make_response(jsonify(ret_body),201 if res_val[0] else 400)
        response.headers['X-Parachutes'] = 'parachutes are cool'  
        return response
