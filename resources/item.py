from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


#every resrouce has to be a class; here's our first resource
class Item(Resource): # so Item iherrits from resrouce
	# moving parser code from ortinal put method below, lets all the methods call it now
	parser = reqparse.RequestParser()  #this ensures we're only dealing with the price, anything else that comes in gets erased;
	parser.add_argument('price',
			type=float,
			required=True,
			help="This field cannont be left blank!"
		)
	parser.add_argument('store_id',
			type=int,
			required=True,
			help="Every item needs a store id"
		)


	@jwt_required() #so before get can be done, user authencation required
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		else:
			return {'message': 'Item not found'}, 404


		# # for item in items:
		# # 	if item['name'] == name:
		# # 		return item
		# item = next(filter(lambda i: i['name'] == name, items), None)	#next on the filter function give us the first item found by the filter functions
		# return {'item': item}, 200 if item else 404 	# remember to return { } always; 404 is to pass along the error code

	# @classmethod
	# def find_by_name(cls, name):
	# 	# now adding data base connection to retrieve item from db
	# 	connection = sqlite3.connect('data.db')
	# 	cursor = connection.cursor()
	#
	# 	query = "SELECT * FROM items WHERE name=?"
	# 	result = cursor.execute(query, (name,))
	# 	row = result.fetchone()
	# 	connection.close()
	# 	# Close the connection to db
	#
	# 	if row is not None:
	# 		return {'item': {'name': row[0], 'price': row[1]}}



	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400 #400 is for bad request

		data = Item.parser.parse_args()

		item = ItemModel(name, data['price'], data['store_id'])

		## ah ha the --- try / except (try/catch?) block for error detection ##
		try:
			item.save_to_db() ## cleaner code, updaed for SQLAlchemy
		except:
			return {"message": "An error occured inserting the item."}, 500 #internal server error




		##usind datbase code above, instead of list append
		# items.append(item)
		return item.json(), 201		# 201 code for created; 202 is accepted if you're delayed in creating the object


	# @classmethod
	# def insert(cls, item):
	# 	connection = sqlite3.connect('data.db')
	# 	cursor = connection.cursor()
	#
	# 	query = "INSERT INTO items VALUES (?, ?)"
	# 	cursor.execute(query, (item['name'], item['price']))
	#
	# 	connection.commit()
	# 	connection.close()


	def delete(self, name):
		#important
		# global items
		# items = list(filter(lambda x: x['name'] != name, items)) ## overwriting original list; with filtered (filtering the global items list), for all items except for the name we'r deleting
		# replaced with db connection

		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {'message': 'The item {} has been deleted'.format(name)}

		## simplified b/c of sqlalchmey
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		#
		# query = "DELETE FROM items WHERE name=?" ##make sure the where is for a unique column
		# cursor.execute(query, (name,))
		#
		# connection.commit()
		# connection.close()
		#
		#
		# return {'message': 'The item {} has been deleted'.format(name)}

	def put(self, name):
		# this creates or updates item

		data = Item.parser.parse_args()

		# item = next(filter(lambda x: x['name'] == name, items), None) #checking items list to see if json data.name is in the list
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json()

			# item = ItemModel(name, data['price'], data['store_id'])
			# try:
			# 	item = ItemModel(name, data['price'])
			#
			# except:
			# 	return {"message": "An error occurred inserting the item."}, 500
			#
			#
			# # items.append(item)

			# try:
			# 	updated_item.update()
			# except:
			# 	return {"message": "An error occurred updating the item."}, 500


			# item.update(data)
		# return updated_item.json()

	# @classmethod
	# def update(cls, item):
	# 	connection = sqlite3.connect('data.db')
	# 	cursor = connection.cursor()
	#
	# 	query = "UPDATE items SET price=? WHERE name=?"
	# 	cursor.execute(query, (item['price'], item['name']))
	#
	# 	connection.commit()
	# 	connection.close()




class ItemList(Resource):
	def get(self):
		return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
		# the list comprehension version of the above is: return {'items': [x.json() for x in ItemModel.query.all()]}

		## now with db connect
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		#
		# query = "SELECT * FROM items"
		# result = cursor.execute(query)
		# items = []
		# for row in result:
		# 	items.append({'name': row[0], 'price': row[1]})
		#
		# connection.close()

		# return {'items': items}
