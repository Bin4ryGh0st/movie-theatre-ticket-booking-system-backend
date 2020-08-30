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

    timestamp = time.ctime()
    show_id = dbutil.add_show(timestamp, generate_show_id())

    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    # print(dbutil.get_show_bookings(show_id))
    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    # print(dbutil.get_show_bookings(show_id))
    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    t = dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    dbutil.book_ticket("a","1111", show_id, timestamp, generate_ticket_id())
    # print(dbutil.get_show_bookings(show_id))
    # print(dbutil.list_shows())
    print(dbutil.get_booking_details(t["Ticket ID"]))

    




