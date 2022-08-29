import curses
from distutils.util import execute
import os
import sqlite3 as lite
from sqlite3 import Error

# database name: account_database.db
# login info table name: account


def create_info_default(path):
    '''
    Create username and password default for app.
    '''
    con = lite.connect(path)
    account_list = [
        ('admin', 'admin', 'admin'),
        ('username1', 'username1', 'user'),
        ('username2', 'username2', 'user')
    ]
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS account')
    cur.execute(
        'CREATE TABLE account(username text, password text, role text)')
    cur.executemany('INSERT INTO account VALUES(?, ?, ?)', account_list)


def create_connection(path_db):
    '''
    Function to check file db exists or not. If not create a new db file.
    '''
    check_db_exist = os.path.exists(path_db)
    if check_db_exist:
        print('Database is exist!')
    else:
        print('Created database file.')
        con = None
        try:
            con = lite.connect(path_db)
            print(lite.version)
        except Error as e:
            print(e)
        finally:
            if con:
                con.close()

        create_info_default(path_db)
