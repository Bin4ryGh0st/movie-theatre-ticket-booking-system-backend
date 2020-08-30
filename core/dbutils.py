import sqlite3

class dbutil():
    def __init__(self):
        self.__database = "db.sqlite3"
        try:
            self.__conn = sqlite3.connect(self.__database)
        except:
            raise ConnectionError('Unable to connect Database')
            
        self.__enable_foreign_key_pragma()

    def __enable_foreign_key_pragma(self):
        enable_foreign_key = '''
        PRAGMA foreign_keys=on;
        '''
        prepare = self.__conn.cursor()
        prepare.execute(enable_foreign_key)
        self.__conn.commit()

    def add_movie(self, timestamp):
        query = '''
        INSERT INTO available_shows (show_time)
        VALUES ( ? );
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query, (timestamp,))
        self.__conn.commit()

    def book_show(self, username, contact, show_time):
        query = '''
        INSERT INTO booked_shows (username, contact, show_time)
        VALUES (?, ?, ?);
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query, (username, contact, show_time,))
        self.__conn.commit()
