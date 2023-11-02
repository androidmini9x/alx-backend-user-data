#!/usr/bin/env python3
'''Logger that parse a log with specific format
'''
from typing import List
import re
import logging
import os
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''returns the log message obfuscated'''
    for field in fields:
        message = re.sub(field+'.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


def get_logger() -> logging.Logger:
    '''Return a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    '''Returns a connector to the database'''
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = MySQLConnection(user=user,
                           password=password,
                           host=host,
                           database=db_name)
    return conn


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records'''
        message = super(RedactingFormatter, self).format(record)
        filtered_msg = filter_datum(self._fields, self.REDACTION,
                                    message, self.SEPARATOR)
        return filtered_msg


def main() -> None:
    '''Return formated & filtered data from database'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    fields = cursor.column_names
    logger = get_logger()
    for row in cursor:
        data = ''.join(
            ['{}={}; '.format(k, v) for k, v in zip(fields, row)]
        )
        logger.info(data.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
