"""
Basic file operations utility module.

This module provides utility functions to handle basic file operations such as:
1. Creating files if they do not exist (including creating directories).
2. Converting a string into a valid filename.
3. Reading content from a file.
4. Overwriting the content of a file.

These functions simplify interaction with the filesystem and can be reused in different projects where file operations are necessary.

Functions:
    - createFileIfNotExists: Creates a file and its parent directories if they don't exist.
    - getValidFileNameForString: Converts a string into a valid filename with the specified file type.
    - readStringFromFile: Reads content from a file and returns it as a string.
    - overwriteContentOfFile: Overwrites the content of a file with a new string.

Usage example:

    # Import the module
    import fileUtils

    # Create a file if it doesn't exist
    fileUtils.createFileIfNotExists("/path/to/file.txt")

    # Get a valid filename from a string
    valid_filename = fileUtils.getValidFileNameForString("Invalid *filename#", "txt")
    print(valid_filename)  # Output: "Invalidfilename.txt"

    # Read content from a file
    content = fileUtils.readStringFromFile("/path/to/file.txt")
    print(content)

    # Overwrite content of a file
    fileUtils.overwriteContentOfFile("/path/to/file.txt", "New content")
"""

import os
import re

def createFileIfNotExists(fileToCreateIfNotExists: str) -> None:
    """
    Creates a file if it does not exist, including any missing directories.

    If the provided path includes directories that don't exist, they will be created with appropriate permissions.
    The file will also be created with 775 permissions if it doesn't already exist.

    Args:
        fileToCreateIfNotExists (str): The full path to the file to be created if it does not exist.

    Raises:
        ValueError: If the provided path does not contain a directory.

    Example:
        createFileIfNotExists("/path/to/file.txt")
    """
    if "/" in fileToCreateIfNotExists:
        lastSlashPosition = fileToCreateIfNotExists.rfind("/")
        directoryName = fileToCreateIfNotExists[:lastSlashPosition]

        if not os.path.exists(directoryName):
            os.makedirs(directoryName)
            os.chmod(directoryName, 0o775)

        if not os.path.exists(fileToCreateIfNotExists):
            os.mknod(fileToCreateIfNotExists)
            os.chmod(fileToCreateIfNotExists, 0o775)
    else:
        raise ValueError("Cannot create a file without a directory (pass filename with full filepath like 'path/to/file.txt')")


def getValidFileNameForString(stringToConvertToFileName: str, fileType: str) -> str:
    """
    Converts a string into a valid filename by removing invalid characters and limiting its length.

    Args:
        stringToConvertToFileName (str): The string to be sanitized and converted into a valid filename.
        fileType (str): The file extension to be added to the filename.

    Returns:
        str: A sanitized and valid filename with the specified file type.

    Example:
        validFilename = getValidFileNameForString("my *invalid filename#", "txt")
        # Output: "myinvalidfilename.txt"
    """
    whiteListedCharactersRegEx = "[^a-zA-Z0-9.\-_]"
    validFilename = re.sub(whiteListedCharactersRegEx, '', str(stringToConvertToFileName))
    validFilename = validFilename[:100]  # Limit the filename to 100 characters.
    return f"{validFilename}.{fileType}"


def readStringFromFile(fileToReadStringFrom: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        fileToReadStringFrom (str): The path to the file to read.

    Returns:
        str: The content of the file as a string.

    Example:
        content = readStringFromFile("/path/to/file.txt")
    """
    with open(fileToReadStringFrom, 'r') as file:
        return file.read().rstrip()


def overwriteContentOfFile(fileToEdit: str, newString: str) -> None:
    """
    Overwrites the content of a file with a new string.

    Note: This will completely remove the previous content of the file.

    Args:
        fileToEdit (str): The path to the file to edit.
        newString (str): The new content to write to the file.

    Example:
        overwriteContentOfFile("/path/to/file.txt", "New content to overwrite the file")
    """
    with open(fileToEdit, 'w') as file:
        file.write(str(newString))
