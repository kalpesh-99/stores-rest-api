import os

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenicate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# using flask_restful we DON"T need to call jsonify

# A resource is the thing our api is about / retrun etc; students, coins, pianos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  #just means the db is in the rood code directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kalsecretkey'
api = Api(app)	#flask is going to be our app, and our app will have routes, but this time also the api; more easily to create resources/api

#this is to auto-create db tables
# @app.before_first_request
# def create_table():
# 	db.create_all()

jwt = JWT(app, authenicate, identity)  # so this creates a new endpoint, ex. /auth, if user is ok, we can send token



@app.route('/') 	## this decorators sets teh the endpoint in this case is the root folder
def home():			#'home' method -- think class baed views?
	return "Hello, Kali!!"



#connecting the resource to the api
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__': 	## this ensures app runs only from intital launch, not on subsequent imports
	from db import db 	#this is done to avoid circular imports by having it up top
	db.init_app(app)
	app.run(port=5000, debug=True)  #debug built-in to flask, creates a html to see errors
