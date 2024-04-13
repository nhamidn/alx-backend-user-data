#!/usr/bin/env python3
"""
filtred_logger module.
"""

import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "ssn", "password", "phone")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init method."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a specified record as text."""
        redacted_message = filter_datum(self.fields, self.REDACTION,
                                        record.getMessage(), self.SEPARATOR)
        record.msg = redacted_message
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function that returns the log message obfuscated."""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """function that returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """function that Returns a connector to a MySQL database."""
    cnx = mysql.connector.connection.MySQLConnection(
      user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
      password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
      host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
      database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return cnx


def main() -> None:
    """main function of the module."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
