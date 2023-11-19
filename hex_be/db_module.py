import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('models/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    return db


def db_exists():
    if sqlite3.connect(current_app.config['DATABASE']) is not None:
        connection = sqlite3.connect(current_app.config['DATABASE'])
        cursor = connection.cursor()
        if cursor is not None:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player';")
            if cursor.fetchone() is not None:
                connection.close()
                return True
        return False
    else:
        return False