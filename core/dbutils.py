import sqlite3
import time
from datetime import datetime

class dbutil():
    def __init__(self):
        '''Initializes the configuration required for DB'''
        self.__database = "db.sqlite3"
        self.__lazy_update_cooldown = 0
        self.MAX_COOLDOWN_REQUEST = 10
        self.TIME_FOR_EXPIRY = 8*60*60
        self.MAX_AVAILABLE_SLOTS = 20

        try:
            self.__conn = sqlite3.connect(self.__database, check_same_thread=False)
        except:
            raise ConnectionError('Unable to connect Database')
            
        self.__enable_foreign_key_pragma()
        self.__lazy_db_update()

    def __enable_foreign_key_pragma(self):
        '''Enables Foreign key PRAGMA in DB to successfully achieve ON DELETE CASCADE'''
        enable_foreign_key = '''
            PRAGMA foreign_keys=on;
        '''
        prepare = self.__conn.cursor()
        prepare.execute(enable_foreign_key)
        self.__conn.commit()

    def __reduce_seat_count(self, show_id, previous_availability):
        '''Reduces the number of total available seats for the give movie show by 1'''
        if previous_availability > 0:
            query = '''
                UPDATE available_shows 
                SET total_bookings = ?
                WHERE show_id = ?;
            '''

            prepare = self.__conn.cursor()
            prepare.execute(query, (previous_availability-1 ,show_id,))
            self.__conn.commit()
    
    def __increase_seat_count(self, show_id, previous_availability):
        '''Increases the number of total available seats for the give movie show by 1'''
        if previous_availability < self.MAX_AVAILABLE_SLOTS:
            query = '''
                UPDATE available_shows 
                SET total_bookings = ?
                WHERE show_id = ?;
            '''

            prepare = self.__conn.cursor()
            prepare.execute(query, (previous_availability+1 ,show_id,))
            self.__conn.commit()

    def __lazy_db_update(self, bypass_cooldown = False):
        ''' Checks for stale/expired movie shows and removes them
            which triggres ON DELETE CASCADE and resulting deletion of stale/expired tickets from DB too.

            Triggers after every self.MAX_COOLDOWN_REQUEST(=10) number of calls to this function or
            Triggered after every 8 hours from add_show in core/dbutils.py
            So in 8 hours or every 10 requests it get triggered and clear expired entries.
            (Win Win!)
        '''
        if self.__lazy_update_cooldown == 0 or bypass_cooldown:
            show_db = self.list_shows()
            stale_show_ids = []
            current_timestamp = datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y") 
            for shows in show_db:
                show_timestamp = datetime.strptime(show_db[shows]["Show Time"], "%a %b %d %H:%M:%S %Y")
                if (current_timestamp-show_timestamp).seconds > self.TIME_FOR_EXPIRY:
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
        self.__lazy_update_cooldown%=self.MAX_COOLDOWN_REQUEST
        
            
    def add_show(self, timestamp, show_id):
        '''Add a new movie show to DB
           Also triggers __lazy_db_update

           Triggered by refine_db_job in main.py in every 8 hours.
        '''
        self.__lazy_db_update(bypass_cooldown=True)
        query = '''
            INSERT INTO available_shows (show_id, show_time)
            VALUES (?, ?);
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query, (show_id, timestamp,))
        self.__conn.commit()
        
        return show_id

    def book_ticket(self, username, contact, show_id, show_time, ticket_id):
        '''
            Book Ticket Functionality Wrappers for DB update.
        '''
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
        '''
            List all available shows Functionality Wrappers for DB.
        '''
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
        '''
            Delete ticket Functionality Wrappers for DB update.
        '''
        query = '''
            DELETE FROM booked_tickets WHERE ticket_id = ? ;
        '''

        prepare = self.__conn.cursor()
        prepare.execute(query, (ticket_id,))

        self.__conn.commit()
        return {"Success" : "Tickect has been deleted iff it was present earlier!"}
        
    def get_show_bookings(self, show_id):
        '''
            List all bookings for particular show Functionality Wrappers for DB.
        '''
        query = '''
            SELECT ticket_id FROM booked_tickets WHERE show_id = ? ;
        '''

        prepare = self.__conn.cursor()
        prepare.execute(query,(show_id,))

        raw_data = prepare.fetchall()

        details = dict()

        counter = 1
        for ticket_id in raw_data:
            details[counter] = ticket_id
            counter+=1
        
        return details
    
    def get_booking_details(self, ticket_id):
        '''
            Get booking/user details using given ticket_id Functionality Wrappers for DB.
        '''
        query = '''
            SELECT * FROM booked_tickets WHERE ticket_id = ? ;
        '''

        prepare = self.__conn.cursor()
        prepare.execute(query,(ticket_id,))

        raw_data = prepare.fetchall()[0]
        try:    
            details = {
                    "User" : raw_data[0],
                    "Contact Number" : raw_data[1],
                    "Show ID" : raw_data[2],
                    "Show Time" : raw_data[3],
                    "Ticket ID" : raw_data[4]
                }
            return details
        except:
            return {"Error" : "Details not found for {}!".format(ticket_id)}

    def get_show_details(self, show_id):
        '''
            Get show details using show_id Functionality Wrappers for DB.
        '''
        query = '''
            SELECT * FROM available_shows WHERE show_id = ? ;
        '''
        prepare = self.__conn.cursor()
        prepare.execute(query,(show_id,))
        raw_data = prepare.fetchall()[0]
        details = {
            "Show ID" : raw_data[0],
            "Show Time" : raw_data[1],
            "Available Slots" : raw_data[2]
        }
        return details

    def change_ticket_timing(self, ticket_id, new_show_id):
        '''
            Update current time of the given ticket to new given show time Functionality Wrappers for DB update.
        '''
        showdb = self.list_shows(show_id_only=True)

        if (new_show_id in showdb) and (showdb[new_show_id] > 0):
            old_show_id = self.get_booking_details(ticket_id)["Show ID"]
            show_details = self.get_show_details(new_show_id)
            query = '''
                UPDATE booked_tickets 
                    SET show_id = ?, show_time = ?
                WHERE 
                    ticket_id = ? ;
            '''
            prepare = self.__conn.cursor()
            prepare.execute(query, (new_show_id, show_details['Show Time'], ticket_id,))
            self.__conn.commit()
            self.__increase_seat_count(old_show_id, showdb[old_show_id])
            self.__reduce_seat_count(new_show_id, showdb[new_show_id])
            
            details = {
                "Success" : True,
                "Ticket ID" : ticket_id,
                "New Show Timing" : show_details['Show Time'] 
            }

            return details 
        else:
            return {"Error" : "Show IDs are incorrect or requested show is HouseFull!"}
