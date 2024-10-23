"""
Logger class for logging information, warnings, and errors.

Logs are written to both day-based files (logs separated by day) and global logs (aggregated over time).
Logs are saved in the following structure:
1. Global error log file (errorlog.txt)
2. Global log file (log.txt)
3. Day-based error log files (one per day)
4. Day-based log files (one per day)

Log entries are timestamped and categorized as INFO, WARNING, or ERROR.

Functions:
    - logError: Logs an error message to all error and log files.
    - logWarning: Logs a warning message to all error and log files.
    - logInformation: Logs an information message to log files.
    - updateDayBasedLogFilePaths: Updates file paths for day-based log files.

Usage example:

    # Initialize the logger
    logger = Logger(logScope="api")

    # Log error, warning, and information messages
    logger.logError("An error occurred")
    logger.logWarning("This is a warning")
    logger.logInformation("This is an info log")
"""

import os
import json
import fileUtils
import dateStringUtils


class Logger:
    """
    Logger class for logging messages (INFO, WARNING, ERROR) into both global and day-based log files.
    
    Attributes:
        logScope (str): The scope of the logger to categorize the log messages.
        logPath (str): The base path for logs.
        globalErrorLogFile (str): Path to the global error log file.
        globalLogFile (str): Path to the global log file.
        dayLogPath (str): Path for day-based logs.
        dayBasedErrorLogFile (str): Path to the current day-based error log file.
        dayBasedLogFile (str): Path to the current day-based log file.
    """

    def __init__(self, logScope: str = None):
        """
        Initializes the Logger class, sets up log paths, and creates necessary log files.

        Args:
            logScope (str, optional): The scope of the logger (e.g., "api"). Defaults to the value in the config.
        """
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        with open(config_file_pathAndName) as config_file:
            config_array = json.load(config_file)

        # Determine log scope (default or custom)
        if logScope is None or logScope.lower() == str(config_array["logger"]["default_logScope"]).lower():
            logScopeStartText = str(config_array["logger"]["default_logScope"]).upper()
            self.logtext_info = f"{logScopeStartText}_INFO"
            self.logtext_warning = f"{logScopeStartText}_WARNING"
            self.logtext_error = f"{logScopeStartText}_ERROR"
        else:
            self.logtext_info = "UNKNOWN_INFO"
            self.logtext_warning = "UNKNOWN_WARNING"
            self.logtext_error = "UNKNOWN_ERROR"

        # Set up log paths and create global log files
        self.logPath = os.path.join(config_array["installPath"], "logs")
        self.globalErrorLogFile = os.path.join(self.logPath, "errorlog.txt")
        self.globalLogFile = os.path.join(self.logPath, "log.txt")
        fileUtils.createFileIfNotExists(self.globalErrorLogFile)
        fileUtils.createFileIfNotExists(self.globalLogFile)

        # Set up day-based log paths
        self.dayLogPath = os.path.join(self.logPath, "dayBased")
        self.updateDayBasedLogFilePaths()

    def updateDayBasedLogFilePaths(self) -> None:
        """
        Updates the file paths for the current day-based log and error log files.
        This method is called before logging to ensure logs are written to the correct day-based files.
        """
        dateStringForLogFileName = dateStringUtils.getDateStringForLogFileName()
        dayBasedErrorLogFileName = f"{dateStringForLogFileName}_errorlog.txt"
        dayBasedLogFileName = f"{dateStringForLogFileName}_log.txt"
        self.dayBasedErrorLogFile = os.path.join(self.dayLogPath, dayBasedErrorLogFileName)
        self.dayBasedLogFile = os.path.join(self.dayLogPath, dayBasedLogFileName)
        fileUtils.createFileIfNotExists(self.dayBasedErrorLogFile)
        fileUtils.createFileIfNotExists(self.dayBasedLogFile)

    def logError(self, errorToLog: str) -> None:
        """
        Logs an error message to the global error log, global log, day-based error log, and day-based log.

        Args:
            errorToLog (str): The error message to be logged.
        """
        self.updateDayBasedLogFilePaths()
        fullLogText = f"\n{dateStringUtils.getDateStringForLogTag()} - [{self.logtext_error}] - [{errorToLog}]"
        self.__log(self.globalErrorLogFile, fullLogText)
        self.__log(self.globalLogFile, fullLogText)
        self.__log(self.dayBasedErrorLogFile, fullLogText)
        self.__log(self.dayBasedLogFile, fullLogText)

    def logWarning(self, warningToLog: str) -> None:
        """
        Logs a warning message to the global error log, global log, day-based error log, and day-based log.

        Args:
            warningToLog (str): The warning message to be logged.
        """
        self.updateDayBasedLogFilePaths()
        fullLogText = f"\n{dateStringUtils.getDateStringForLogTag()} - [{self.logtext_warning}] - [{warningToLog}]"
        self.__log(self.globalErrorLogFile, fullLogText)
        self.__log(self.globalLogFile, fullLogText)
        self.__log(self.dayBasedErrorLogFile, fullLogText)
        self.__log(self.dayBasedLogFile, fullLogText)

    def logInformation(self, informationToLog: str) -> None:
        """
        Logs an information message to the global log and day-based log.

        Args:
            informationToLog (str): The information message to be logged.
        """
        self.updateDayBasedLogFilePaths()
        fullLogText = f"\n{dateStringUtils.getDateStringForLogTag()} - [{self.logtext_info}] - [{informationToLog}]"
        self.__log(self.globalLogFile, fullLogText)
        self.__log(self.dayBasedLogFile, fullLogText)

    def __log(self, file: str, fullLogText: str) -> None:
        """
        Private helper function to append a log entry to a specified file.

        Args:
            file (str): The file path to write the log entry to.
            fullLogText (str): The full log entry string.
        """
        with open(file, 'a+') as f:
            f.write(fullLogText)
