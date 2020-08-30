import os
import time
from core import setupdb,dbutils




if __name__ == '__main__':
    if not os.path.exists("db.sqlite3"):
        '''
        Initializes Database if doesn't exists
        '''
        setupdb.init()
    
    dbutil = dbutils.dbutil()

    timestamp = time.ctime()
    dbutil.add_movie(timestamp)
    dbutil.book_show("asdf", "9414", timestamp)    


