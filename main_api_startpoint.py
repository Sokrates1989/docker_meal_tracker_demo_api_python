from typing import Union, List

from fastapi import FastAPI, Response, status
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# For getting config.
import json

# Import own classes.
# Insert path to own stuff to allow importing them.
import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(__file__), "src/", "utils"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "src/", "models"))

# Database Connection.
import databaseWrapper as DatabaseWrapper

# Export database.
import exportUtils as ExportUtils

# Logger.
import logger as Logger

# AuthenticationItem from own models to use location independent.
import authenticationItem as AuthenticationItem

# CredentialsItem from own models to use location independent.
import credentialsItem as CredentialsItem

# Get authentication settings from config file.
config_file_pathAndName = os.path.join(os.path.dirname(__file__), "config.txt")
config_file = open(config_file_pathAndName)
config_array = json.load(config_file)

dbWrapper = DatabaseWrapper.DatabaseWrapper()
logger = Logger.Logger()


# StateCheckItem as pydantic model to use with fastAPI.
# To unify usage, this model should be converted to StateCheckItem asap.
# @see convertPydanticModelToStateCheckItem().
class AuthenticationItem_pydantic(BaseModel):
    token: str


# CredentialsItem as pydantic model to use with fastAPI.
# To unify usage, this model should be converted to CredentialsItem asap.
# @see convertPydanticModelToCredentialsItem().
class CredentialsItem_pydantic(BaseModel):
    token: str
    userName: str
    hashedPassword: str


# Instantiate Fast api.
app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
])


@app.get("/")
async def root_get():
    logger.logInformation("/root_get: 200: called")
    return {"message": "https://github.com/Sokrates1989/docker_api_engaige_meal_tracker_demo.git"}


@app.post("/")
async def root_post():
    logger.logInformation("/root_post: 200: called")
    return {"message": "https://github.com/Sokrates1989/docker_api_engaige_meal_tracker_demo.git"}


# DEBUG Test the token.
@app.post("/v1/token")
async def token(authenticationItem_pydantic: AuthenticationItem_pydantic, response: Response):
    authenticationItem = convertPydanticModel_to_AuthenticationItem(authenticationItem_pydantic)
    if authenticationItem.token == config_array["authentication"]["token"]:
        logger.logInformation("/v1/token: 200: valid token: " + authenticationItem.toString())
        return {"message": "valid token"}
    else:
        response.status_code = 401
        logger.logWarning("/v1/token: 401: invalid token: " + authenticationItem.toString())
        return {"message": "invalid token"}


# Register a new user.
@app.post("/v1/register")
async def register(credentialsItem_pydantic: CredentialsItem_pydantic, response: Response):
    credentialsItem = convertPydanticModel_to_CredentialsItem(credentialsItem_pydantic)
    if credentialsItem.token == config_array["authentication"]["token"]:
        createUserReturn = dbWrapper.createUser(credentialsItem)
        if createUserReturn is None:
            response.status_code = 406
            logger.logWarning("/v1/register: 406: user already exists: " + credentialsItem.toString())
            return {"message": "user already exists"}
        elif createUserReturn == False:
            response.status_code = 401
            logger.logWarning("/v1/register: 401: invalid token: " + credentialsItem.toString())
            return {"message": "invalid token"}
        else:
            response.status_code = 200
            logger.logInformation("/v1/register: 200: successfully registered user: " + credentialsItem.toString())
            return createUserReturn

    else:
        response.status_code = 401
        logger.logWarning("/v1/register: 401: invalid token: " + credentialsItem.toString())
        return {"message": "invalid token"}



# Verify user login.
@app.post("/v1/login")
async def login(credentialsItem_pydantic: CredentialsItem_pydantic, response: Response):
    credentialsItem = convertPydanticModel_to_CredentialsItem(credentialsItem_pydantic)
    if credentialsItem.token == config_array["authentication"]["token"]:
        loginUserReturn = dbWrapper.isUserPasswordCorrect(credentialsItem)
        if loginUserReturn is None:
            response.status_code = 406
            logger.logWarning("/v1/login: 406: user does not exist: " + credentialsItem.toString())
            return {"message": "user does not exist"}
        elif loginUserReturn == False:
            response.status_code = 401
            logger.logWarning("/v1/login: 401: invalid token: " + credentialsItem.toString())
            return {"message": "invalid token"}
        elif loginUserReturn == "invalid password":
            response.status_code = 401
            logger.logWarning("/v1/login: 401: invalid password: " + credentialsItem.toString())
            return {"message": "invalid password"}
        elif loginUserReturn == True:
            userReturn = dbWrapper.getUserByName(credentialsItem.token, credentialsItem.userName)
            if userReturn is None:
                response.status_code = 406
                logger.logWarning("/v1/login: 406: user does not exist: " + credentialsItem.toString())
                return {"message": "user does not exist"}
            elif userReturn == False:
                response.status_code = 401
                logger.logWarning("/v1/login: 401: invalid token: " + credentialsItem.toString())
                return {"message": "invalid token"}
            else:
                response.status_code = 200
                logger.logInformation("/v1/login: 200: successfully logged user in: " + credentialsItem.toString())
                return userReturn
        else:
            response.status_code = 500
            logger.logError("/v1/login: 500: unhandled return from login method: " + credentialsItem.toString())
            return {"message": "unhandled return from login method"}

    else:
        response.status_code = 401
        logger.logWarning("/v1/login: 401: invalid token: " + credentialsItem.toString())
        return {"message": "invalid token"}



# Converts pydantic AuthenticationItem_pydantic to AuthenticationItem.
def convertPydanticModel_to_AuthenticationItem(authenticationItem_pydantic: AuthenticationItem_pydantic):
    authenticationItem = AuthenticationItem.AuthenticationItem(
        authenticationItem_pydantic.token
    )
    return authenticationItem


# Converts pydantic CredentialsItem_pydantic to CredentialsItem.
def convertPydanticModel_to_CredentialsItem(credentialsItem_pydantic: CredentialsItem_pydantic):
    credentialsItem = CredentialsItem.CredentialsItem(
        credentialsItem_pydantic.token,
        credentialsItem_pydantic.userName,
        credentialsItem_pydantic.hashedPassword
    )
    return credentialsItem
