import sqlite3 	#so User class can interact with sqllite
from flask_restful import Resource, reqparse
from models.user import UserModel



## This is the resource for User
class UserRegister(Resource):
	parser = reqparse.RequestParser()  #this ensures we're only dealing with the price, anything else that comes in gets erased;
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannont be left blank!"
	)

	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannont be left blank!"
	)

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']) is not None:
			return {"message": "Sorry that username already exists."}, 400

		user = UserModel(**data)
		user.save_to_db()

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		#
		# query = "INSERT INTO users VALUES (NULL, ?, ?)"    #null b/c int id auto increments
		# cursor.execute(query, (data['username'], data['password'],))
		#
		# connection.commit()
		# connection.close()

		return {"messsage": "User created successfully."}, 201
