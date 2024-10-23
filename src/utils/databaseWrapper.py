"""
DatabaseWrapper module for handling all database interactions.

This module provides the `DatabaseWrapper` class, which is responsible for all interactions with the database. It provides
methods for accessing different repositories (e.g., users, meals, days) and performs operations such as connecting to the
database and validating tokens.

Repositories:
    - UserRepo: Handles user-related operations.
    - DayRepo: Handles day-related operations.
    - MealRepo: Handles meal-related operations.
    - MealTypeRepo: Handles meal type-related operations.
    - DayMealRepo: Handles day-meal-related operations.

Usage example:

    # Import the DatabaseWrapper class
    import databaseWrapper as DatabaseWrapper

    # Initialize the database wrapper
    db_wrapper = DatabaseWrapper.DatabaseWrapper()

    # Access repositories
    user_repo = db_wrapper.getUserRepo()
    meal_repo = db_wrapper.getMealRepo()

    # Validate a token
    is_valid = db_wrapper.isTokenValid("someToken")
"""

import mysql.connector
import json
import time
import os
import sys

# Insert path to allow importing own classes and repositories.
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "..", "utils"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "..", "models"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "repositories"))

# Repositories containing logical parts.
import userRepo as UserRepo
import dayRepo as DayRepo
import mealRepo as MealRepo
import mealTypeRepo as MealTypeRepo
import dayMealRepo as DayMealRepo

# CredentialsItem from own models to use location independent.
import credentialsItem as CredentialsItem


class DatabaseWrapper:
    """
    Wrapper class for all interactions with the database.

    This class establishes a connection with the database and provides access to various repositories
    (user, meal, day, etc.) for performing read and write operations. It also handles tasks like token validation
    and managing encryption keys.

    Attributes:
        dbConnection: MySQL database connection object.
        dbCursor: MySQL database cursor used to execute SQL queries.
        validToken: The predefined token used for authentication.
        encryptionKey: The encryption key used for user data encryption.
    """

    def __init__(self):
        """
        Initializes the DatabaseWrapper by establishing a connection to the database
        and setting the database cursor, token, and encryption key from the configuration file.
        """
        # Get database credentials from the config file.
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        with open(config_file_pathAndName) as config_file:
            config_array = json.load(config_file)

        # Establish the database connection.
        self.dbConnection = mysql.connector.connect(
            host=config_array["database"]["host"],
            user=config_array["database"]["user"],
            password=config_array["database"]["password"],
            database=config_array["database"]["database"],
            port=config_array["database"]["port"]
        )
        self.dbCursor = self.dbConnection.cursor(buffered=True)  # Buffered to fix unread result error.
        self.validToken = config_array["authentication"]["token"]
        self.encryptionKey = config_array["authentication"]["encryption_key"]

    def updateOwnClassVars(self):
        """
        Updates class variables like the database connection and cursor by reloading
        credentials from the configuration file.
        """
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        with open(config_file_pathAndName) as config_file:
            config_array = json.load(config_file)

        # Re-establish the database connection.
        self.dbConnection = mysql.connector.connect(
            host=config_array["database"]["host"],
            user=config_array["database"]["user"],
            password=config_array["database"]["password"],
            database=config_array["database"]["database"],
            port=config_array["database"]["port"]
        )
        self.dbCursor = self.dbConnection.cursor(buffered=True)

        print("Database: Updated own class vars")

    def getUserRepo(self) -> UserRepo.UserRepo:
        """
        Returns an instance of the UserRepo class.

        Returns:
            UserRepo: An instance of the UserRepo class.
        """
        return UserRepo.UserRepo(self)

    def getDayRepo(self) -> DayRepo.DayRepo:
        """
        Returns an instance of the DayRepo class.

        Returns:
            DayRepo: An instance of the DayRepo class.
        """
        return DayRepo.DayRepo(self)

    def getMealRepo(self) -> MealRepo.MealRepo:
        """
        Returns an instance of the MealRepo class.

        Returns:
            MealRepo: An instance of the MealRepo class.
        """
        return MealRepo.MealRepo(self)

    def getMealTypeRepo(self) -> MealTypeRepo.MealTypeRepo:
        """
        Returns an instance of the MealTypeRepo class.

        Returns:
            MealTypeRepo: An instance of the MealTypeRepo class.
        """
        return MealTypeRepo.MealTypeRepo(self)

    def getDayMealRepo(self) -> DayMealRepo.DayMealRepo:
        """
        Returns an instance of the DayMealRepo class.

        Returns:
            DayMealRepo: An instance of the DayMealRepo class.
        """
        return DayMealRepo.DayMealRepo(self)

    def isTokenValid(self, token: str) -> bool:
        """
        Validates whether the provided token matches the validToken.

        Args:
            token (str): The token to be validated.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        return token == self.validToken
