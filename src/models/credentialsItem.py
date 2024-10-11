## Model used to wrap user sent to api.

# Json model of a valid AuthenticationItem to send to the api.
# {
#   "token": "IOdeFyatMDKyCUmVqtQkk4eGcnBYvvGp6aCakzj0ZdSBBtCfGrQvGn8RSbHuJO7RaI6jzGqDq2zmYNaYwY1NHUQJ7xCtPzblGt96",
#   "userName": "SomeName",
#   "hashedPassword": "hashedPWForSomeName"
# }


class CredentialsItem:

    # Constructor.
    def __init__(self, token, userName, hashedPassword):
        self.token = token
        self.userName = userName
        self.hashedPassword = hashedPassword

    def toString(self):
        tokenLength = len(str(self.token))
        hashedPasswordLength = len(str(self.hashedPassword))

        classAsString = 'UserItem{'
        if tokenLength < 3:
            classAsString += '"token":INVALID_LENGTH---PASSED:"' + str(self.token) + '", '
        else:
            classAsString += '"token":"' + str(self.token)[0:3] + '---XXX---' + str(self.token)[
                tokenLength - 3:] + '", '
        classAsString += '"userName":"' + str(self.userName) + '", '
        if hashedPasswordLength < 3:
            classAsString += '"hashedPassword":INVALID_LENGTH---PASSED:"' + str(
                self.hashedPassword) + '", '
        else:
            classAsString += '"hashedPassword":"' + str(self.hashedPassword)[0:3] + '---XXX---' + \
                             str(self.hashedPassword)[hashedPasswordLength - 3:] + '", '

        # Remove last , from string.
        if classAsString[-2:] == ", ":
            classAsString = classAsString[:-2]

        classAsString += '}'

        return classAsString
