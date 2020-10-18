# using flask_restful 
#collect req pip freeze > requirements.txt
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from datetime import datetime
import re
from api import users
from api import user
from api import games


import logging
import logging.config
logging.config.fileConfig('logging.conf')
logging.getLogger(__name__)



app = Flask(__name__)
api = Api(app)

# adding the defined resources along with their corresponding urls 
api.add_resource(user.User, '/users/<int:user_id>')
api.add_resource(users.Users, '/users') 



api.add_resource(games.Games, '/games') 
api.add_resource(games.Game, '/games/<int:game_id>')
api.add_resource(games.GameUser, '/games/<int:game_id>/<int:user_id>')

# @app.route('/')
# def index():
#     print ("rr")
#     return "This is an example app"


# @app.route("/hello/<name>")
# def hello_there(name):
#     now = datetime.now()
#     formatted_now = now.strftime("%A, %d %B, %Y at %X")

#     # Filter the name argument to letters only using regular expressions. URL arguments
#     # can contain arbitrary text, so we restrict to safe characters only.
#     match_object = re.match("[a-zA-Z]+", name)

#     if match_object:
#         clean_name = match_object.group(0)
#     else:
#         clean_name = "Friend"

#     content = "Hello there, " + clean_name + "! It's " + formatted_now
#     return content

# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 