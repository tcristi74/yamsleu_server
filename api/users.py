from flask_restful import Resource,abort,reqparse
from flask import jsonify,request,Response,make_response
import json 
from data.db_user import DbUser
from data.db_config import DbConfig

class Users(Resource):

    def get(self): 
        return jsonify({'message': 'get all users'}) 

    # Corresponds to POST request 
    def post(self): 
        data = request.get_json()     # status code

        parser = reqparse.RequestParser()
        parser.add_argument('type', help='detail or summary')
        #parser.add_argument('year',type=int, help='detail or summary')
        args = parser.parse_args()
        # db_user  = 
        
        db_user = DbUser(DbConfig())
        res_val = db_user.post_user(data)
        ret_body = {"success": res_val[0]}
        if not res_val[0]:
            ret_body["error"] = res_val[1]

        response = make_response(jsonify(ret_body),201 if res_val[0] else 400)
        response.headers['X-Parachutes'] = 'parachutes are cool'  
        return response
