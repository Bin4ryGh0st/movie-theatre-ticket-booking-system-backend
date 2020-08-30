import sqlite3


def init():
    # try:
    database = "db.sqlite3"
    conn = sqlite3.connect(database)

    init_table_available_shows = ''' 
    CREATE TABLE IF NOT EXISTS available_shows(
        show_time TIMESTAMP NOT NULL PRIMARY KEY
        );
    '''

    init_table_booked_shows = '''
    CREATE TABLE IF NOT EXISTS booked_shows(
        username TEXT NOT NULL,
        contact TEXT NOT NULL,
        show_time TIMESTAMP NOT NULL,
        FOREIGN KEY (show_time) 
        REFERENCES available_shows(show_time)
        ON DELETE CASCADE
        );
    '''

    if conn is not None:
        prepare = conn.cursor()
        prepare.execute(init_table_available_shows)

        prepare = conn.cursor()
        prepare.execute(init_table_booked_shows)

    # except Exception as e:
        # print("[Following Eception occured while initializing database] :", e)


if __name__ == '__main__':
    init()