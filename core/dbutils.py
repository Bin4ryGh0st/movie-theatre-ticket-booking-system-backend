import sqlite3
import time
from datetime import datetime

class dbutil():
    def __init__(self):
        self.__database = "db.sqlite3"
        try:
            self.__conn = sqlite3.connect(self.__database)
        except:
            raise ConnectionError('Unable to connect Database')
            
        self.__enable_foreign_key_pragma()
        self.__lazy_update_cooldown = 0
        self.__lazy_db_update()

    def __enable_foreign_key_pragma(self):
        enable_foreign_key = '''
        PRAGMA foreign_keys=on;
        '''
        prepare = self.__conn.cursor()
        prepare.execute(enable_foreign_key)
        self.__conn.commit()

    def __reduce_seat_count(self, show_id, previous_availability):
        query = '''
            UPDATE available_shows 
            SET total_bookings = ?
            WHERE show_id = ?;
        '''

        prepare = self.__conn.cursor()
        prepare.execute(query, (previous_availability-1 ,show_id,))
        self.__conn.commit()

    def __lazy_db_update(self):
        MAX_COOLDOWN_REQUEST = 10
        if self.__lazy_update_cooldown == 0:
            TIME_FOR_EXPIRY = 8*60*60
            TIME_FOR_EXPIRY = 20
            show_db = self.list_shows()
            stale_show_ids = []
            current_timestamp = datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y") 
            for shows in show_db:
                show_timestamp = datetime.strptime(show_db[shows]["Show Time"], "%a %b %d %H:%M:%S %Y")
                if (current_timestamp-show_timestamp).seconds > TIME_FOR_EXPIRY:
                    stale_show_ids.append(show_db[shows]["Show ID"])
            query = '''
                DELETE FROM available_shows 
                WHERE show_id = ?;
            '''
            for stale_show_id in stale_show_ids:
                prepare = self.__conn.cursor()
                prepare.execute(query, (stale_show_id,))
                self.__conn.commit()
        self.__lazy_update_cooldown+=1
        self.__lazy_update_cooldown%=MAX_COOLDOWN_REQUEST
        
            
    def add_movie(self, timestamp, show_id):
        query = '''
        INSERT INTO available_shows (show_id, show_time)
        VALUES (?, ?);
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query, (show_id, timestamp,))
        self.__conn.commit()
        
        return show_id

    def book_ticket(self, username, contact, show_id, show_time, ticket_id):
        self.__lazy_db_update()
        show_db = self.list_shows(show_id_only=True)

        if (show_id in show_db) and show_db[show_id]!=0:
            query = '''
            INSERT INTO booked_tickets (username, contact, show_id, show_time, ticket_id)
            VALUES (?, ?, ?, ?, ?);
            '''

            prepare = self.__conn.cursor()
            prepare.execute(query, (username, contact, show_id, show_time, ticket_id,))
            self.__conn.commit()

            details = {
                "User" : username,
                "Contact Number" : contact,
                "Show ID" : show_id,
                "Show Time" : show_time,
                "Ticket ID" : ticket_id
            }

            self.__reduce_seat_count(show_id, int(show_db[show_id]))

            return details
        else:
            return {"Error" : "Incorrect Show ID or Movie already is HouseFull!"}

    def list_shows(self, show_id_only = False):
        query = '''
        SELECT * FROM available_shows; 
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query)

        raw_data = prepare.fetchall()
        
        details = dict()

        if show_id_only:
            for show_id,timestamp,available_slots  in raw_data:
                details[show_id] = available_slots
            return details
        else:
            counter = 1
            for show_id,timestamp,available_slots  in raw_data:
                details[counter] = dict()
                details[counter]["Show ID"] = show_id
                details[counter]["Show Time"] = timestamp
                details[counter]["Available Slots"] = available_slots
                counter+=1
            return details
    
    def delete_ticket(self, ticket_id):
        query = '''
        DELETE FROM booked_tickets WHERE ticket_id = ? ;
        '''

        prepare = self.__conn.cursor()
        prepare.execute(query, (ticket_id,))

        self.__conn.commit()
        

