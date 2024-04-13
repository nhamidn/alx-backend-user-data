#!/usr/bin/env python3
"""

Filtered Datum

"""


from os import getenv
from typing import List
import logging
import mysql.connector
import re


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
        >> Returns an obscured log message.
        >> fields: representing all fields to obfuscate.
        >> redaction: representing by what the field will be obfuscated.
        >> message: representing the log line.
        >> separator: representing by which character is separating...
           all fields in the log line (message).
    """
    regex = '|'.join(f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
        >> Redacting Formatter class: accepts a list..
           of strings fields constructor argument.
        >> Redacts specified fields from log records.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            >> Filters values in incoming log records using filter_datum.
            >> Values for fields in fields should be filtered.
            >> Do not extrapolate FORMAT manually.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
        >> Creates a Logger object with specific settings.
    """
    logger = logging.getLogger("user_data")  # should be named "user_data"
    logger.setLevel(logging.INFO)  # only log up to logging.INFO level.
    logger.propagate = False  # should not propagate messages to other loggers.
    # It should have a StreamHandler with RedactingFormatter as formatter.
    stream_handler = logging.StreamHandler()
    # PII_FIELDS: contains the fields from user_data.csv..
    # ..that are considered PII.
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        >> A connector to the database.
        >> using environment variables for connection details.
        >> Return:
           > MySQLConnection: A connection object to the MySQL database.
    """
    db_connection = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )

    return db_connection


def main():
    """
        >> This function will obtain a database connection using "get_db"
        >> Retrieves all rows in the users table,
        >> Displays each row under a filtered format.
    """
    mydatabase = get_db()
    cursor = mydatabase.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [idx[0] for idx in cursor.description]
    logger = get_logger()
    for r in cursor:
        row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(row.strip())

    cursor.close()
    mydatabase.close()
