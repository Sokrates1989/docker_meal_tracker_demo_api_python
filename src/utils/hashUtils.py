# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

"""
Utilities for password and login operations using hash algorithms.

This module provides functions to securely hash passwords using the SHA-512 hash algorithm with the inclusion of a pepper
and an optional salt. The purpose of this is to ensure secure password handling in login-like scenarios.

Functions:
    - getSha512: Generates a SHA-512 hash of the given password, pepper, and salt.

Usage example:
    # Import the module
    import hashUtils

    # Hash a password with a pepper and optional salt
    hashed_password = hashUtils.getSha512("myPassword", "myPepper")
    print(hashed_password)

    # Hash a password with a custom salt
    hashed_password_with_salt = hashUtils.getSha512("myPassword", "myPepper", "myCustomSalt")
    print(hashed_password_with_salt)
"""

import hashlib

def getSha512(password: str, pepper: str, salt: str = "aSDh7u8o134z5890712374ß9v571ß293vß9qe&123801348509134985§124889137") -> str:
    """
    Generates a SHA-512 hash of the given password, pepper, and salt.

    Args:
        password (str): The password to be hashed.
        pepper (str): The pepper (a secret value added to the password) for additional security.
        salt (str, optional): The salt (a random string) to be added to the password and pepper for further security. 
                              Defaults to a predefined salt.

    Returns:
        str: The SHA-512 hash of the combined password, pepper, and salt as a hexadecimal string.

    Example:
        hashed_password = getSha512("myPassword", "myPepper")
        hashed_password_with_salt = getSha512("myPassword", "myPepper", "myCustomSalt")
    """
    # Combine password, pepper, and salt
    stringToHash = password + pepper + salt
    
    # Create a SHA-512 hash object and return the hexadecimal digest
    hash_object = hashlib.sha512(stringToHash.encode())  # Ensure encoding to bytes
    hex_dig = hash_object.hexdigest()
    
    return hex_dig
