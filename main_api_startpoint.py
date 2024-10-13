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

# Logger.
import logger as Logger

# AuthenticationItem from own models to use location independent.
import authenticationItem as AuthenticationItem

# Own models to use location independent.
import credentialsItem as CredentialsItem
import getMealsItem as GetMealsItem
import mealItem as MealItem
import deleteMealItem as DeleteMealItem

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


class MealItem_pydantic(BaseModel):
    credentials: CredentialsItem_pydantic
    year: int
    month: int
    day: int
    mealType: str  # 'breakfast', 'lunch', 'dinner', 'snacks'
    fat_level: int  # 0: Low, 1: Medium, 2: High
    sugar_level: int  # 0: Low, 1: Medium, 2: High

class DeleteMealItem_pydantic(BaseModel):
    credentials: CredentialsItem_pydantic
    year: int
    month: int
    day: int
    mealType: str  # 'breakfast', 'lunch', 'dinner', 'snacks'


class GetMealsItem_pydantic(BaseModel):
    credentials: CredentialsItem_pydantic
    year: int
    month: int
    day: int


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



@app.post("/db_check")
async def db_check(response: Response):
    amountServices = dbWrapper.getServiceRepo().getAmountOfServices()
    if amountServices == False:
        response.status_code = 503
        logger.logError("/db_check: 503: amountServices is False")
        return {"message": "Did not retrieve valid query return"}
    elif isinstance(amountServices, int):
        response.status_code = 200
        logger.logInformation("db_check: 200: api IS UP")
        return {"message": "api is Up"}
    else:
        response.status_code = 503
        logger.logError("db_check: 503: Unknown error executing db_check")
        return {"message": "Unknown error executing db_check"}


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
        createUserReturn = dbWrapper.getUserRepo().createNewUser_fromCredentialsItem(credentialsItem)
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
    return login_local(credentialsItem_pydantic, response)

def login_local(credentialsItem_pydantic: CredentialsItem_pydantic, response: Response, alreadyAttemptedToUpdateOwnClassVars=False):
    credentialsItem = convertPydanticModel_to_CredentialsItem(credentialsItem_pydantic)

    if credentialsItem.token == config_array["authentication"]["token"]:
        loginUserReturn = dbWrapper.getUserRepo().isUserPasswordCorrect(credentialsItem)
        if loginUserReturn is None:

            # User might have just been created, but since db is buffered we need to ensure, to have the most current db.
            if credentialsItem.userName == "" or alreadyAttemptedToUpdateOwnClassVars == True:
                response.status_code = 406
                logger.logWarning("/v1/login: 406: user does not exist: " + credentialsItem.toString())
                return {"message": "user does not exist"}
            else:
                dbWrapper.updateOwnClassVars()
                return login_local(credentialsItem_pydantic, response, True)

        elif loginUserReturn == False:
            response.status_code = 401
            logger.logWarning("/v1/login: 401: invalid token: " + credentialsItem.toString())
            return {"message": "invalid token"}
        elif loginUserReturn == "invalid password":
            response.status_code = 401
            logger.logWarning("/v1/login: 401: invalid password: " + credentialsItem.toString())
            return {"message": "invalid password"}
        elif loginUserReturn == True:
            userReturn = dbWrapper.getUserRepo().getUserByCredentialsItem(credentialsItem)
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
    


# API Endpoint for adding a meal
@app.post("/v1/addMeal")
async def addMeal(mealItem_pydantic: MealItem_pydantic, response: Response):
    mealItem = convertPydanticModel_to_MealItem(mealItem_pydantic)

    # Check if token is valid
    if mealItem.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning("/v1/addMeal: 401: invalid token: " + mealItem.credentialsItem.toString())
        return {"message": "invalid token"}

    # Verify user login
    loginUserReturn = dbWrapper.getUserRepo().isUserPasswordCorrect(mealItem.credentialsItem)
    if loginUserReturn == True:
        user = dbWrapper.getUserRepo().getUserByCredentialsItem(mealItem.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning("/v1/addMeal: 406: user does not exist: " + mealItem.credentialsItem.toString())
            return {"message": "user does not exist"}
        userID = user["ID"]

        # Add meal
        dayRepo = dbWrapper.getDayRepo()
        day = dayRepo.getDayByDate(mealItem.year, mealItem.month, mealItem.day)
        if day is None:
            day = dayRepo.createNewDay(mealItem.year, mealItem.month, mealItem.day)
        dayID = day["ID"]

        mealTypeRepo = dbWrapper.getMealTypeRepo()
        mealTypeID = mealTypeRepo.getMealTypeIDByName(mealItem.mealType.lower())
        if mealTypeID is None:
            response.status_code = 400
            logger.logWarning("/v1/addMeal: 400: invalid meal type: " + mealItem.mealType)
            return {"message": "invalid meal type"}

        mealRepo = dbWrapper.getMealRepo()
        meal = mealRepo.createNewMeal(mealItem.fat_level, mealItem.sugar_level)
        mealID = meal["ID"]

        dayMealRepo = dbWrapper.getDayMealRepo()
        dayMeal = dayMealRepo.createNewDayMeal(userID, dayID, mealTypeID, mealID)
        if dayMeal is None:
            response.status_code = 400
            logger.logWarning("/v1/addMeal: 400: could not create day meal")
            return {"message": "Meal already exists. To edit meal use /v1/editMeal"}

        response.status_code = 200
        logger.logInformation("/v1/addMeal: 200: successfully added meal")
        return {"message": "successfully added meal"}

    elif loginUserReturn == False:
        response.status_code = 401
        logger.logWarning("/v1/addMeal: 401: invalid token: " + mealItem.credentialsItem.toString())
        return {"message": "invalid token"}
    elif loginUserReturn == "invalid password":
        response.status_code = 401
        logger.logWarning("/v1/addMeal: 401: invalid password: " + mealItem.credentialsItem.toString())
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/addMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}
    

# API Endpoint for editing a meal
@app.post("/v1/editMeal")
async def editMeal(mealItem_pydantic: MealItem_pydantic, response: Response):
    mealItem = convertPydanticModel_to_MealItem(mealItem_pydantic)

    # Check if token is valid
    if mealItem.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning("/v1/editMeal: 401: invalid token: " + mealItem.credentialsItem.toString())
        return {"message": "invalid token"}

    # Verify user login
    loginUserReturn = dbWrapper.getUserRepo().isUserPasswordCorrect(mealItem.credentialsItem)
    if loginUserReturn == True:
        user = dbWrapper.getUserRepo().getUserByCredentialsItem(mealItem.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning("/v1/editMeal: 406: user does not exist: " + mealItem.credentialsItem.toString())
            return {"message": "user does not exist"}
        userID = user["ID"]

        # Get the day by date
        dayRepo = dbWrapper.getDayRepo()
        day = dayRepo.getDayByDate(mealItem.year, mealItem.month, mealItem.day)
        if day is None:
            response.status_code = 404
            logger.logWarning("/v1/editMeal: 404: day not found")
            return {"message": "day not found"}
        dayID = day["ID"]

        # Get the meal type
        mealTypeRepo = dbWrapper.getMealTypeRepo()
        mealTypeID = mealTypeRepo.getMealTypeIDByName(mealItem.mealType.lower())
        if mealTypeID is None:
            response.status_code = 400
            logger.logWarning("/v1/editMeal: 400: invalid meal type: " + mealItem.mealType)
            return {"message": "invalid meal type"}

        # Get the existing meal
        dayMealRepo = dbWrapper.getDayMealRepo()
        existingDayMeal = dayMealRepo.getDayMeal(userID, dayID, mealTypeID)
        if existingDayMeal is None:
            response.status_code = 404
            logger.logWarning("/v1/editMeal: 404: meal not found for the specified day")
            return {"message": "meal not found for the specified day"}

        # Get the meal ID
        mealID = existingDayMeal["fk_meal_id"]

        # Update the meal
        mealRepo = dbWrapper.getMealRepo()
        updateResult = mealRepo.updateMeal(mealID, mealItem.fat_level, mealItem.sugar_level)
        if updateResult == True:
            response.status_code = 200
            logger.logInformation("/v1/editMeal: 200: successfully edited meal")
            return {"message": "successfully edited meal"}
        else:
            response.status_code = 500
            logger.logError("/v1/editMeal: 500: failed to update meal")
            return {"message": "failed to update meal"}

    elif loginUserReturn == False:
        response.status_code = 401
        logger.logWarning("/v1/editMeal: 401: invalid token: " + mealItem.credentialsItem.toString())
        return {"message": "invalid token"}
    elif loginUserReturn == "invalid password":
        response.status_code = 401
        logger.logWarning("/v1/editMeal: 401: invalid password: " + mealItem.credentialsItem.toString())
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/editMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}
    

# API Endpoint for deleting a meal.
@app.post("/v1/deleteMeal")
async def deleteMeal(deleteMealItem_pydantic: DeleteMealItem_pydantic, response: Response):
    deleteMealItem = convertPydanticModel_to_DeleteMealItem(deleteMealItem_pydantic)

    # Check if token is valid
    if deleteMealItem.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning("/v1/deleteMeal: 401: invalid token: " + deleteMealItem.credentialsItem.toString())
        return {"message": "invalid token"}

    # Verify user login
    loginUserReturn = dbWrapper.getUserRepo().isUserPasswordCorrect(deleteMealItem.credentialsItem)
    if loginUserReturn == True:
        user = dbWrapper.getUserRepo().getUserByCredentialsItem(deleteMealItem.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning("/v1/deleteMeal: 406: user does not exist: " + deleteMealItem.credentialsItem.toString())
            return {"message": "user does not exist"}
        userID = user["ID"]

        # Get the day by date
        dayRepo = dbWrapper.getDayRepo()
        day = dayRepo.getDayByDate(deleteMealItem.year, deleteMealItem.month, deleteMealItem.day)
        if day is None:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: day not found")
            return {"message": "day not found"}
        dayID = day["ID"]

        # Get the meal type
        mealTypeRepo = dbWrapper.getMealTypeRepo()
        mealTypeID = mealTypeRepo.getMealTypeIDByName(deleteMealItem.mealType.lower())
        if mealTypeID is None:
            response.status_code = 400
            logger.logWarning("/v1/deleteMeal: 400: invalid meal type: " + deleteMealItem.mealType)
            return {"message": "invalid meal type"}

        # Get the existing meal in day_meals
        dayMealRepo = dbWrapper.getDayMealRepo()
        existingDayMeal = dayMealRepo.getDayMeal(userID, dayID, mealTypeID)
        if existingDayMeal is None:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: meal not found for the specified day")
            return {"message": "meal not found for the specified day"}

        # Get the meal ID
        mealID = existingDayMeal["fk_meal_id"]

        # Delete the meal and day_meals entry
        deleteResult = dbWrapper.getMealRepo().deleteMeal(userID, dayID, mealTypeID, mealID)
        if deleteResult == True:
            response.status_code = 200
            logger.logInformation("/v1/deleteMeal: 200: successfully deleted meal and day_meal entry")
            return {"message": "successfully deleted meal"}
        elif deleteResult == False:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: meal or day_meal entry not found")
            return {"message": "meal or day_meal entry not found"}
        else:
            response.status_code = 500
            logger.logError("/v1/deleteMeal: 500: unknown error occurred during deletion")
            return {"message": "unknown error occurred"}

    elif loginUserReturn == False:
        response.status_code = 401
        logger.logWarning("/v1/deleteMeal: 401: invalid token: " + deleteMealItem.credentialsItem.toString())
        return {"message": "invalid token"}
    elif loginUserReturn == "invalid password":
        response.status_code = 401
        logger.logWarning("/v1/deleteMeal: 401: invalid password: " + deleteMealItem.credentialsItem.toString())
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/deleteMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}



# API Endpoint for getting meals for a user.
@app.post("/v1/getMeals")
async def getMeals(getMealsItem_pydantic: GetMealsItem_pydantic, response: Response):
    getMealsItem = convertPydanticModel_to_GetMealsItem(getMealsItem_pydantic)

    # Check if token is valid
    if getMealsItem.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning("/v1/getMeals: 401: invalid token: " + getMealsItem.credentialsItem.toString())
        return {"message": "invalid token"}

    # Verify user login
    loginUserReturn = dbWrapper.getUserRepo().isUserPasswordCorrect(getMealsItem.credentialsItem)
    if loginUserReturn == True:
        user = dbWrapper.getUserRepo().getUserByCredentialsItem(getMealsItem.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning("/v1/getMeals: 406: user does not exist: " + getMealsItem.credentialsItem.toString())
            return {"message": "user does not exist"}
        userID = user["ID"]

        # Get meals
        dayRepo = dbWrapper.getDayRepo()
        day = dayRepo.getDayByDate(getMealsItem.year, getMealsItem.month, getMealsItem.day)
        if day is None:
            response.status_code = 404
            logger.logWarning("/v1/getMeals: 404: day not found")
            return {"message": "day not found"}
        dayID = day["ID"]

        dayMealRepo = dbWrapper.getDayMealRepo()
        dayMeals = dayMealRepo.getDayMealsByUserIDAndDayID(userID, dayID)
        mealList = []
        mealTypeRepo = dbWrapper.getMealTypeRepo()
        mealRepo = dbWrapper.getMealRepo()

        for dayMeal in dayMeals:
            mealTypeID = dayMeal['fk_meal_type_id']
            mealID = dayMeal['fk_meal_id']

            mealTypeName = mealTypeRepo.getMealTypeNameByID(mealTypeID)
            if mealTypeName is None:
                continue

            meal = mealRepo.getMealByID(mealID)
            if meal is None:
                continue

            mealInfo = {
                'year': getMealsItem.year,
                'month': getMealsItem.month,
                'day': getMealsItem.day,
                'mealType': mealTypeName,
                'fat_level': meal['fat_level'],
                'sugar_level': meal['sugar_level'],
            }
            mealList.append(mealInfo)

        response.status_code = 200
        logger.logInformation("/v1/getMeals: 200: successfully retrieved meals")
        return {"meals": mealList}
    

# API Endpoint for getting all meal types.
@app.post("/v1/getMealTypes")
async def getMealTypes(credentials: CredentialsItem_pydantic, response: Response):
    try:
        # Validate token
        if credentials.token != config_array["authentication"]["token"]:
            response.status_code = 401
            logger.logWarning("/v1/getMealTypes: 401: invalid token")
            return {"message": "invalid token"}

        # Fetch meal types
        mealTypes = dbWrapper.getMealTypeRepo().getAllMealTypes()
        if mealTypes is None:
            response.status_code = 500
            logger.logError("/v1/getMealTypes: 500: error fetching meal types")
            return {"message": "error fetching meal types"}

        response.status_code = 200
        logger.logInformation("/v1/getMealTypes: 200: successfully fetched meal types")
        return {"mealTypes": mealTypes}

    except Exception as e:
        response.status_code = 500
        logger.logError(f"/v1/getMealTypes: 500: unhandled exception: {str(e)}")
        return {"message": "unhandled exception"}




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


# Converts pydantic MealItem_pydantic to MealItem.
def convertPydanticModel_to_MealItem(mealItem_pydantic: MealItem_pydantic):
    credentialsItem = convertPydanticModel_to_CredentialsItem(mealItem_pydantic.credentials)
    return MealItem.MealItem(
        credentialsItem,
        mealItem_pydantic.year,
        mealItem_pydantic.month,
        mealItem_pydantic.day,
        mealItem_pydantic.mealType,
        mealItem_pydantic.fat_level,
        mealItem_pydantic.sugar_level
    )

def convertPydanticModel_to_DeleteMealItem(deleteMealItem_pydantic: DeleteMealItem_pydantic):
    credentialsItem = convertPydanticModel_to_CredentialsItem(deleteMealItem_pydantic.credentials)
    return DeleteMealItem.DeleteMealItem(
        credentialsItem,
        deleteMealItem_pydantic.year,
        deleteMealItem_pydantic.month,
        deleteMealItem_pydantic.day,
        deleteMealItem_pydantic.mealType
    )

# Converts pydantic GetMealsItem_pydantic to GetMealsItem.
def convertPydanticModel_to_GetMealsItem(getMealsItem_pydantic: GetMealsItem_pydantic):
    credentialsItem = convertPydanticModel_to_CredentialsItem(getMealsItem_pydantic.credentials)
    return GetMealsItem.GetMealsItem(
        credentialsItem,
        getMealsItem_pydantic.year,
        getMealsItem_pydantic.month,
        getMealsItem_pydantic.day
    )

