## this will be the internal representatin of the item
## The find_by_username, find_by_id and insert methods are used inside (not called by api)
## so lets move them here into the models

from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))    #The ForeignKey relates many items to a store
    store = db.relationship('StoreModel')


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()     #this line translates to SQL: SELECT * FROM items WHERE name=name LIMIT 1

        ## below code is replaced with SQLAlchemy code above
        # now adding data base connection to retrieve item from db
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # # Close the connection to db
        #
        # if row is not None:
        # 	return cls(*row) #cls(row[0], row[1])

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #def insert(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def update(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name)
        # connection.commit()
        # connection.close()
