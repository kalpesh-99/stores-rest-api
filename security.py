from werkzeug.security import safe_str_cmp #compares strings to make sure they are same, takes care of diff encodings
from models.user import UserModel

####### User list and mapping replaced by user.py class User #############
# users = [
	# {
	# 	'id': 1,
	# 	'username': 'bob',
	# 	'password': 'temp'
	# }
	## now that we have imported User class
# 	User(1, 'bob', 'temp')

# ]


# username_mapping = {u.username: u for u in users} ## ok simplifed from the dict below,

	# 'bob': {
	# 	'id': 1,
	# 	'username': 'bob',
	# 	'password': 'temp'

	# }



# userid_mapping = {u.id: u for u in users}
# 	1: {
# 		'id': 1,
# 		'username': 'bob',
# 		'password': 'temp'

# 	}
# }
####### User list and mapping replaced by user.py class User #############


# create authentication function
def authenicate(username, password):
	user = UserModel.find_by_username(username)		#get is another way to access dictionary // replacing "username_mapping.get(username, None)" with new User method accessing db
	if user and safe_str_cmp(user.password, password):
		return user

def identity(payload):
	user_id = payload['identity']
	return UserModel.find_by_id(user_id) # replacing "userid_mapping.get(user_id, None)" with new User method that calls db
