# import sqlite3 	#so User class can interact with sqllite
from db import db

# we will create a class called user to define users, this class can't be used as the resuorce
class UserModel(db.Model):
	__tablename__ = 'users' #for db SQLAlchemy setup

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))	#max username length
	password = db.Column(db.String(80))


	def __init__(self, username, password):
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod #makes the code a bit nicer, as we're not using 'self' in the method
	def find_by_username(cls, username):		## ths is a function that will find users in our db
		return cls.query.filter_by(username=username).first()  #note (cls, username) is =username

		# connection = sqlite3.connect('data.db')	## create the connection
		# cursor = connection.cursor()
		#
		# query = "SELECT * FROM users WHERE username=?"	## this is the table we're looking at; all (*) fields of users
		# result = cursor.execute(query, (username,)) 	## important 2nd paramter is a tuple so needs the ,)
		# row = result.fetchone()		## so, result has the cursor, that lets us itterate on it, here we just want one
		# if row:
		# 	# user = User(row[0], row[1], row[2]) // code below is nicer
		# 	user = cls(*row)
		# else:
		# 	user = None
		#
		# connection.close()		#no commit line required because we're not writing to tb only reading here.
		# return user


	@classmethod
	def find_by_id(cls, _id):		## to create a simlar mapping function based on id this time
		return cls.query.filter_by(id=_id).first()

		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		#
		# query = "SELECT * FROM users WHERE id=?"
		# result = cursor.execute(query, (_id,))
		# row = result.fetchone()
		# if row:
		# 	# user = User(row[0], row[1], row[2]) // code below is nicer
		# 	user = cls(*row)
		# else:
		# 	user = None
		#
		# connection.close()		#no commit line required because we're not writing to tb only reading here.
		# return user
