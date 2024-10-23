"""
Date-based string utility functions.

This module provides utility functions for generating date and time strings formatted for specific purposes, such as:
1. Log file names (format: 'YYYY_MM_DD').
2. Log tags that include both date and time (format: '[YYYY-MM-DD HH:MM:SS]').

These functions are useful for applications that involve logging or need date-specific file naming conventions.

Functions:
    - getDateStringForLogFileName: Returns the current date formatted for use in log file names.
    - getDateStringForLogTag: Returns the current date and time formatted for use in log tags.

Usage example:
    # Import the module
    import dateStringUtils

    # Get the current date string for a log file name
    log_file_name = dateStringUtils.getDateStringForLogFileName()

    # Get the current date and time for a log tag
    log_tag = dateStringUtils.getDateStringForLogTag()
"""

from datetime import datetime
import time

def getDateStringForLogFileName() -> str:
    """
    Returns the current date in the format 'YYYY_MM_DD' suitable for log file names.

    Returns:
        str: The current date as a string in the format 'YYYY_MM_DD'.
    """
    now = datetime.now()
    return now.strftime("%Y_%m_%d")

def getDateStringForLogTag() -> str:
    """
    Returns the current date and time in the format '[YYYY-MM-DD HH:MM:SS]' suitable for log tags.

    Returns:
        str: The current date and time as a string in the format '[YYYY-MM-DD HH:MM:SS]'.
    """
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"[{date_time}]"
