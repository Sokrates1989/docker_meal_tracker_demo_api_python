"""
FastAPI-based module for handling meal tracking API endpoints.

This module provides the core functionality for managing user authentication, registration, 
and meal tracking operations such as adding, editing, and deleting meals. It uses Pydantic models 
to validate incoming requests and interacts with a MySQL database using custom repositories.

Module includes:
    - Authentication (token validation)
    - User registration and login
    - Meal operations (add, edit, delete, and retrieve meals)
    - Fetching available meal types

Dependencies:
    - FastAPI
    - Pydantic
    - Custom imports (databaseWrapper, logger, models like MealItem and GetMealsItem)

Usage example:

    # Import the module
    import databaseWrapper as DatabaseWrapper
    import logger as Logger

    # Initialize components
    db_wrapper = DatabaseWrapper.DatabaseWrapper()
    logger = Logger.Logger()

    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Public imports.
from fastapi import FastAPI, Response
from pydantic import BaseModel
import json
import os

# Custom imports for database, logger, and models
import databaseWrapper as DatabaseWrapper
import logger as Logger
import authenticationItem as AuthenticationItem
import credentialsItem as CredentialsItem
import getMealsItem as GetMealsItem
import mealItem as MealItem
import deleteMealItem as DeleteMealItem

# Configuration setup
config_file_path = os.path.join(os.path.dirname(__file__), "config.txt")
with open(config_file_path, 'r') as config_file:
    config_array = json.load(config_file)

# Initialize database wrapper and logger
db_wrapper = DatabaseWrapper.DatabaseWrapper()
logger = Logger.Logger()

app = FastAPI()

# Models
class AuthenticationItemPydantic(BaseModel):
    """Represents authentication data for validation."""
    token: str


class CredentialsItemPydantic(BaseModel):
    """Represents credentials for a user."""
    token: str
    userName: str
    hashedPassword: str


class MealItemPydantic(BaseModel):
    """Represents a meal entry for a specific day and meal type."""
    credentials: CredentialsItemPydantic
    year: int
    month: int
    day: int
    mealType: str
    fat_level: int  # 0: Low, 1: Medium, 2: High
    sugar_level: int  # 0: Low, 1: Medium, 2: High


class DeleteMealItemPydantic(BaseModel):
    """Represents data required to delete a meal."""
    credentials: CredentialsItemPydantic
    year: int
    month: int
    day: int
    mealType: str


class GetMealsItemPydantic(BaseModel):
    """Represents the details for fetching meals for a user on a specific day."""
    credentials: CredentialsItemPydantic
    year: int
    month: int
    day: int

@app.post("/v1/token")
async def token(authentication_item: AuthenticationItemPydantic, response: Response):
    """Validates the provided token and returns a response."""
    auth_item = convert_pydantic_to_authentication_item(authentication_item)
    if auth_item.token == config_array["authentication"]["token"]:
        logger.logInformation(f"/v1/token: 200: valid token: {auth_item}")
        return {"message": "valid token"}
    else:
        response.status_code = 401
        logger.logWarning(f"/v1/token: 401: invalid token: {auth_item}")
        return {"message": "invalid token"}


@app.post("/v1/register")
async def register(credentials_item: CredentialsItemPydantic, response: Response):
    """Registers a new user if token validation passes."""
    credentials = convert_pydantic_to_credentials_item(credentials_item)
    if credentials.token == config_array["authentication"]["token"]:
        create_user_result = db_wrapper.getUserRepo().createNewUser_fromCredentialsItem(credentials)
        if create_user_result is None:
            response.status_code = 406
            logger.logWarning(f"/v1/register: 406: user already exists: {credentials}")
            return {"message": "user already exists"}
        elif create_user_result is False:
            response.status_code = 401
            logger.logWarning(f"/v1/register: 401: invalid token: {credentials}")
            return {"message": "invalid token"}
        else:
            response.status_code = 200
            logger.logInformation(f"/v1/register: 200: successfully registered user: {credentials}")
            return create_user_result
    else:
        response.status_code = 401
        logger.logWarning(f"/v1/register: 401: invalid token: {credentials}")
        return {"message": "invalid token"}


@app.post("/v1/login")
async def login(credentials_item: CredentialsItemPydantic, response: Response):
    """Verifies user login credentials."""
    return login_local(credentials_item, response)


def login_local(credentials_item: CredentialsItemPydantic, response: Response, attempted_update=False):
    """Handles local login logic."""
    credentials = convert_pydantic_to_credentials_item(credentials_item)
    if credentials.token == config_array["authentication"]["token"]:
        login_result = db_wrapper.getUserRepo().isUserPasswordCorrect(credentials)
        if login_result is None:
            if credentials.userName == "" or attempted_update:
                response.status_code = 406
                logger.logWarning(f"/v1/login: 406: user does not exist: {credentials}")
                return {"message": "user does not exist"}
            else:
                db_wrapper.updateOwnClassVars()
                return login_local(credentials_item, response, True)
        elif login_result is False:
            response.status_code = 401
            logger.logWarning(f"/v1/login: 401: invalid token: {credentials}")
            return {"message": "invalid token"}
        elif login_result == "invalid password":
            response.status_code = 401
            logger.logWarning(f"/v1/login: 401: invalid password: {credentials}")
            return {"message": "invalid password"}
        else:
            user = db_wrapper.getUserRepo().getUserByCredentialsItem(credentials)
            if user is None:
                response.status_code = 406
                logger.logWarning(f"/v1/login: 406: user does not exist: {credentials}")
                return {"message": "user does not exist"}
            response.status_code = 200
            logger.logInformation(f"/v1/login: 200: successfully logged user in: {credentials}")
            return user
    else:
        response.status_code = 401
        logger.logWarning(f"/v1/login: 401: invalid token: {credentials}")
        return {"message": "invalid token"}


@app.post("/v1/addMeal")
async def add_meal(meal_item: MealItemPydantic, response: Response):
    """Adds a new meal entry."""
    meal = convert_pydantic_to_meal_item(meal_item)

    # Validate token
    if meal.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning(f"/v1/addMeal: 401: invalid token: {meal.credentialsItem}")
        return {"message": "invalid token"}

    # Verify user login
    login_result = db_wrapper.getUserRepo().isUserPasswordCorrect(meal.credentialsItem)
    if login_result is True:
        user = db_wrapper.getUserRepo().getUserByCredentialsItem(meal.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning(f"/v1/addMeal: 406: user does not exist: {meal.credentialsItem}")
            return {"message": "user does not exist"}

        user_id = user["ID"]
        day_repo = db_wrapper.getDayRepo()
        day = day_repo.getDayByDate(meal.year, meal.month, meal.day)
        if day is None:
            day = day_repo.createNewDay(meal.year, meal.month, meal.day)
        day_id = day["ID"]

        meal_type_repo = db_wrapper.getMealTypeRepo()
        meal_type_id = meal_type_repo.getMealTypeIDByName(meal.mealType.lower())
        if meal_type_id is None:
            response.status_code = 400
            logger.logWarning(f"/v1/addMeal: 400: invalid meal type: {meal.mealType}")
            return {"message": "invalid meal type"}

        meal_repo = db_wrapper.getMealRepo()
        new_meal = meal_repo.createNewMeal(meal.fat_level, meal.sugar_level)
        meal_id = new_meal["ID"]

        day_meal_repo = db_wrapper.getDayMealRepo()
        day_meal = day_meal_repo.createNewDayMeal(user_id, day_id, meal_type_id, meal_id)
        if day_meal is None:
            response.status_code = 400
            logger.logWarning(f"/v1/addMeal: 400: could not create day meal")
            return {"message": "Meal already exists. To edit meal use /v1/editMeal"}

        response.status_code = 200
        logger.logInformation("/v1/addMeal: 200: successfully added meal")
        return {"message": "successfully added meal"}

    elif login_result is False:
        response.status_code = 401
        logger.logWarning(f"/v1/addMeal: 401: invalid token: {meal.credentialsItem}")
        return {"message": "invalid token"}
    elif login_result == "invalid password":
        response.status_code = 401
        logger.logWarning(f"/v1/addMeal: 401: invalid password: {meal.credentialsItem}")
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/addMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}


@app.post("/v1/editMeal")
async def edit_meal(meal_item: MealItemPydantic, response: Response):
    """Edits an existing meal entry."""
    meal = convert_pydantic_to_meal_item(meal_item)

    # Validate token
    if meal.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning(f"/v1/editMeal: 401: invalid token: {meal.credentialsItem}")
        return {"message": "invalid token"}

    # Verify user login
    login_result = db_wrapper.getUserRepo().isUserPasswordCorrect(meal.credentialsItem)
    if login_result is True:
        user = db_wrapper.getUserRepo().getUserByCredentialsItem(meal.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning(f"/v1/editMeal: 406: user does not exist: {meal.credentialsItem}")
            return {"message": "user does not exist"}

        user_id = user["ID"]
        day_repo = db_wrapper.getDayRepo()
        day = day_repo.getDayByDate(meal.year, meal.month, meal.day)
        if day is None:
            response.status_code = 404
            logger.logWarning("/v1/editMeal: 404: day not found")
            return {"message": "day not found"}
        day_id = day["ID"]

        meal_type_repo = db_wrapper.getMealTypeRepo()
        meal_type_id = meal_type_repo.getMealTypeIDByName(meal.mealType.lower())
        if meal_type_id is None:
            response.status_code = 400
            logger.logWarning(f"/v1/editMeal: 400: invalid meal type: {meal.mealType}")
            return {"message": "invalid meal type"}

        day_meal_repo = db_wrapper.getDayMealRepo()
        existing_day_meal = day_meal_repo.getDayMeal(user_id, day_id, meal_type_id)
        if existing_day_meal is None:
            response.status_code = 404
            logger.logWarning("/v1/editMeal: 404: meal not found for the specified day")
            return {"message": "meal not found for the specified day"}

        meal_id = existing_day_meal["fk_meal_id"]
        meal_repo = db_wrapper.getMealRepo()
        update_result = meal_repo.updateMeal(meal_id, meal.fat_level, meal.sugar_level)
        if update_result is True:
            response.status_code = 200
            logger.logInformation("/v1/editMeal: 200: successfully edited meal")
            return {"message": "successfully edited meal"}
        else:
            response.status_code = 500
            logger.logError("/v1/editMeal: 500: failed to update meal")
            return {"message": "failed to update meal"}

    elif login_result is False:
        response.status_code = 401
        logger.logWarning(f"/v1/editMeal: 401: invalid token: {meal.credentialsItem}")
        return {"message": "invalid token"}
    elif login_result == "invalid password":
        response.status_code = 401
        logger.logWarning(f"/v1/editMeal: 401: invalid password: {meal.credentialsItem}")
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/editMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}


@app.post("/v1/deleteMeal")
async def delete_meal(delete_meal_item: DeleteMealItemPydantic, response: Response):
    """Deletes a meal entry."""
    delete_meal = convert_pydantic_to_delete_meal_item(delete_meal_item)

    # Validate token
    if delete_meal.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning(f"/v1/deleteMeal: 401: invalid token: {delete_meal.credentialsItem}")
        return {"message": "invalid token"}

    # Verify user login
    login_result = db_wrapper.getUserRepo().isUserPasswordCorrect(delete_meal.credentialsItem)
    if login_result is True:
        user = db_wrapper.getUserRepo().getUserByCredentialsItem(delete_meal.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning(f"/v1/deleteMeal: 406: user does not exist: {delete_meal.credentialsItem}")
            return {"message": "user does not exist"}

        user_id = user["ID"]
        day_repo = db_wrapper.getDayRepo()
        day = day_repo.getDayByDate(delete_meal.year, delete_meal.month, delete_meal.day)
        if day is None:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: day not found")
            return {"message": "day not found"}
        day_id = day["ID"]

        meal_type_repo = db_wrapper.getMealTypeRepo()
        meal_type_id = meal_type_repo.getMealTypeIDByName(delete_meal.mealType.lower())
        if meal_type_id is None:
            response.status_code = 400
            logger.logWarning(f"/v1/deleteMeal: 400: invalid meal type: {delete_meal.mealType}")
            return {"message": "invalid meal type"}

        day_meal_repo = db_wrapper.getDayMealRepo()
        existing_day_meal = day_meal_repo.getDayMeal(user_id, day_id, meal_type_id)
        if existing_day_meal is None:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: meal not found for the specified day")
            return {"message": "meal not found for the specified day"}

        meal_id = existing_day_meal["fk_meal_id"]
        delete_result = db_wrapper.getMealRepo().deleteMeal(user_id, day_id, meal_type_id, meal_id)
        if delete_result is True:
            response.status_code = 200
            logger.logInformation("/v1/deleteMeal: 200: successfully deleted meal and day_meal entry")
            return {"message": "successfully deleted meal"}
        elif delete_result is False:
            response.status_code = 404
            logger.logWarning("/v1/deleteMeal: 404: meal or day_meal entry not found")
            return {"message": "meal or day_meal entry not found"}
        else:
            response.status_code = 500
            logger.logError("/v1/deleteMeal: 500: unknown error occurred during deletion")
            return {"message": "unknown error occurred"}

    elif login_result is False:
        response.status_code = 401
        logger.logWarning(f"/v1/deleteMeal: 401: invalid token: {delete_meal.credentialsItem}")
        return {"message": "invalid token"}
    elif login_result == "invalid password":
        response.status_code = 401
        logger.logWarning(f"/v1/deleteMeal: 401: invalid password: {delete_meal.credentialsItem}")
        return {"message": "invalid password"}
    else:
        response.status_code = 500
        logger.logError("/v1/deleteMeal: 500: unhandled return from login method")
        return {"message": "unhandled return from login method"}


@app.post("/v1/getMeals")
async def get_meals(get_meals_item: GetMealsItemPydantic, response: Response):
    """Fetches the meal entries for a user on a specific day."""
    get_meals = convert_pydantic_to_get_meals_item(get_meals_item)

    # Validate token
    if get_meals.credentialsItem.token != config_array["authentication"]["token"]:
        response.status_code = 401
        logger.logWarning(f"/v1/getMeals: 401: invalid token: {get_meals.credentialsItem}")
        return {"message": "invalid token"}

    # Verify user login
    login_result = db_wrapper.getUserRepo().isUserPasswordCorrect(get_meals.credentialsItem)
    if login_result is True:
        user = db_wrapper.getUserRepo().getUserByCredentialsItem(get_meals.credentialsItem)
        if user is None:
            response.status_code = 406
            logger.logWarning(f"/v1/getMeals: 406: user does not exist: {get_meals.credentialsItem}")
            return {"message": "user does not exist"}

        user_id = user["ID"]
        day_repo = db_wrapper.getDayRepo()
        day = day_repo.getDayByDate(get_meals.year, get_meals.month, get_meals.day)
        if day is None:
            # No day exists, meaning no meals exist for that day
            response.status_code = 200
            logger.logInformation("/v1/getMeals: 200: empty meal list (no day found)")
            return {"meals": []}
        day_id = day["ID"]

        day_meal_repo = db_wrapper.getDayMealRepo()
        day_meals = day_meal_repo.getDayMealsByUserIDAndDayID(user_id, day_id)
        meal_list = []
        meal_type_repo = db_wrapper.getMealTypeRepo()
        meal_repo = db_wrapper.getMealRepo()

        for day_meal in day_meals:
            meal_type_id = day_meal["fk_meal_type_id"]
            meal_id = day_meal["fk_meal_id"]

            meal_type_name = meal_type_repo.getMealTypeNameByID(meal_type_id)
            if meal_type_name is None:
                continue

            meal = meal_repo.getMealByID(meal_id)
            if meal is None:
                continue

            meal_info = {
                "year": get_meals.year,
                "month": get_meals.month,
                "day": get_meals.day,
                "mealType": meal_type_name,
                "fat_level": meal["fat_level"],
                "sugar_level": meal["sugar_level"],
            }
            meal_list.append(meal_info)

        response.status_code = 200
        logger.logInformation("/v1/getMeals: 200: successfully retrieved meals")
        return {"meals": meal_list}


@app.post("/v1/getMealTypes")
async def get_meal_types(credentials: CredentialsItemPydantic, response: Response):
    """Fetches all available meal types."""
    try:
        # Validate token
        if credentials.token != config_array["authentication"]["token"]:
            response.status_code = 401
            logger.logWarning("/v1/getMealTypes: 401: invalid token")
            return {"message": "invalid token"}

        # Fetch meal types
        meal_types = db_wrapper.getMealTypeRepo().getAllMealTypes()
        if meal_types is None:
            response.status_code = 500
            logger.logError("/v1/getMealTypes: 500: error fetching meal types")
            return {"message": "error fetching meal types"}

        response.status_code = 200
        logger.logInformation("/v1/getMealTypes: 200: successfully fetched meal types")
        return {"mealTypes": meal_types}

    except Exception as e:
        response.status_code = 500
        logger.logError(f"/v1/getMealTypes: 500: unhandled exception: {str(e)}")
        return {"message": "unhandled exception"}


# Helper functions for converting Pydantic models to internal models
def convert_pydantic_to_authentication_item(auth_pydantic: AuthenticationItemPydantic):
    """Converts a Pydantic AuthenticationItem model to the internal AuthenticationItem."""
    return AuthenticationItem.AuthenticationItem(auth_pydantic.token)


def convert_pydantic_to_credentials_item(credentials_pydantic: CredentialsItemPydantic):
    """Converts a Pydantic CredentialsItem model to the internal CredentialsItem."""
    return CredentialsItem.CredentialsItem(
        credentials_pydantic.token,
        credentials_pydantic.userName,
        credentials_pydantic.hashedPassword
    )


def convert_pydantic_to_meal_item(meal_pydantic: MealItemPydantic):
    """Converts a Pydantic MealItem model to the internal MealItem."""
    credentials_item = convert_pydantic_to_credentials_item(meal_pydantic.credentials)
    return MealItem.MealItem(
        credentials_item,
        meal_pydantic.year,
        meal_pydantic.month,
        meal_pydantic.day,
        meal_pydantic.mealType,
        meal_pydantic.fat_level,
        meal_pydantic.sugar_level
    )


def convert_pydantic_to_delete_meal_item(delete_meal_pydantic: DeleteMealItemPydantic):
    """Converts a Pydantic DeleteMealItem model to the internal DeleteMealItem."""
    credentials_item = convert_pydantic_to_credentials_item(delete_meal_pydantic.credentials)
    return DeleteMealItem.DeleteMealItem(
        credentials_item,
        delete_meal_pydantic.year,
        delete_meal_pydantic.month,
        delete_meal_pydantic.day,
        delete_meal_pydantic.mealType
    )


def convert_pydantic_to_get_meals_item(get_meals_pydantic: GetMealsItemPydantic):
    """Converts a Pydantic GetMealsItem model to the internal GetMealsItem."""
    credentials_item = convert_pydantic_to_credentials_item(get_meals_pydantic.credentials)
    return GetMealsItem.GetMealsItem(
        credentials_item,
        get_meals_pydantic.year,
        get_meals_pydantic.month,
        get_meals_pydantic.day
    )
