import os
import sqlite3

def connect(db_name):
    '''
        Create connection with DB
    '''
    conn = sqlite3.connect(db_name)
    return conn

def create_schema(conn, query):
    '''
        Execute given SQLite query
    '''
    prepare = conn.cursor()
    prepare.execute(query)
    conn.commit()

def init():
    '''
    Automated initialization of the Database
    and Schemas for Movie Ticket Booking System
    '''
    try:
        database = "db.sqlite3"
        conn = connect(database)

        enable_foreign_key = '''
        PRAGMA foreign_keys=on;
        '''

        MAX_AVAILABLE_SLOTS = 20

        init_table_available_shows = ''' 
        CREATE TABLE IF NOT EXISTS available_shows(
            show_id TEXT NOT NULL PRIMARY KEY,
            show_time TIMESTAMP NOT NULL,
            total_bookings INTEGER DEFAULT {}
            );
        '''.format(MAX_AVAILABLE_SLOTS)

        init_table_booked_tickets = '''
        CREATE TABLE IF NOT EXISTS booked_tickets(
            username TEXT NOT NULL,
            contact TEXT NOT NULL,
            show_id TEXT NOT NULL,
            show_time TIMESTAMP NOT NULL,
            ticket_id TEXT NOT NULL PRIMARY KEY,
            CONSTRAINT fk_available_shows
                FOREIGN KEY (show_id) 
                REFERENCES available_shows(show_id)
                ON DELETE CASCADE
            );
        '''

        if conn is not None:
            create_schema(conn, enable_foreign_key)
            create_schema(conn, init_table_available_shows)
            create_schema(conn, init_table_booked_tickets)


    except Exception as e:
        print("[Following Eception occured while initializing database] :", e)

