import logging
import sqlite3
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def connect_db():
    ok = False

    try:
        db = create_engine(current_db['use'] + '://' + current_db['path'])
        db.connect()
    except OperationalError as err:
        if current_db['use'] == 'postgres':
            logging.warning("PostgreSQL connection error. Falling back to SQLite.")
            current_db['use'] = 'sqlite'
            set_current_db()
            create()

    if db:
        ok = True

    return db, ok

