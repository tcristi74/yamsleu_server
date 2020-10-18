from flask_restful import Resource,abort,reqparse
from flask import jsonify,request,Response,make_response
import json 
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Game(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
  
    def get(self,game_id): 
        if (game_id!='cristi'):
            return jsonify({'message': f'get {name} user'})
        else: 
            abort(404, message=json.dumps({'message':"user doesn't exit"}))

    def put(self,name): 
        data = request.get_json()     # status code
        return Response(None,status=204)




class Games(Resource):

    def get(self): 
        return jsonify({'message': 'get all users'}) 

    # Corresponds to POST request 
    def post(self): 
        data = request.get_json()     # status code

        parser = reqparse.RequestParser()
        parser.add_argument('type', help='detail or summary')
        #parser.add_argument('year',type=int, help='detail or summary')
        args = parser.parse_args()
        # for k in request.args.keys():
        #     print (k,request.args[k])
        response = make_response(jsonify(data),201)
        response.headers['X-Parachutes'] = 'parachutes are cool'  
        return response
