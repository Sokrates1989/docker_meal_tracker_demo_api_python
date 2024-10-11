## Model used to wrap authentication settings sent to api.

# Json model of a valid AuthenticationItem to send to the api.
# {
#   "token": "IOdeFyatMDKyCUmVqtQkk4eGcnBYvvGp6aCakzj0ZdSBBtCfGrQvGn8RSbHuJO7RaI6jzGqDq2zmYNaYwY1NHUQJ7xCtPzblGt96"
# }


class AuthenticationItem:

	# Constructor.
	def __init__(self, token):
		self.token = token

	def toString(self):
		tokenLength = len(str(self.token))

		classAsString = 'AuthenticationItem{'
		if tokenLength < 3:
			classAsString += '"token":INVALID_LENGTH---PASSED:"' + str(self.token) + '"'
		else:
			classAsString += '"token":"' + str(self.token)[0:3] + '---XXX---' + str(self.token)[tokenLength - 3:] + '"'
		classAsString += '}'

		return classAsString