import os
import time
import hashlib
from core import setupdb,dbutils


def generate_ticket_id():
    return hashlib.sha256(str(time.time()).encode()+os.urandom(16)).hexdigest()

def generate_show_id():
    return hashlib.md5(str(time.time()).encode()+os.urandom(16)).hexdigest()

if __name__ == '__main__':
    if not os.path.exists("db.sqlite3"):
        '''
        Initializes Database instance if doesn't exists
        '''
        setupdb.init()
    else:
        pass
    
    dbutil = dbutils.dbutil()
    print(dbutil.list_shows())
    




