# Movie Theatre Ticket Booking System Backend
---
## Zomentum Hiring Challenge (Backend)

### Functionality :
1. Endpoint for booking movie ticket for available shows.
  * $POST /book
2. Endpoint to update ticket timings.
  * PUT /update/<ticket_id>/new/show/id/<new_show_id>
3. Endpoint to view all tickets for particular show.
  * GET /list/all/tickets/for/show/<show_id>
4. Endpoint to delete particular ticket.
  * DELETE /delete/ticket/<ticket_id>
5. Endpoint to view the user’s details based on the ticket id.
  * GET /detail/<ticket_id>
6. Deletes expired shows/tickets from database using following techniques : 
  a. Lazy update : Triggers refining of database after every 10th(Variable) request to it.
  b. Scheduler : A parallel thread which triggers refining of database after every 8 hours(variable).
  c. ON DELETE CASCADE in database while creating schema which deletes all the expired tickets if the show is deleted itself using following query :
    `'''
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
        '''`
### Techstack Used :
1. Python3
2. Flask Microframework for creating WEB APIs.
3. SQLite3 for data storage and manupulation purposes.

#### Setup Procedure:
    $ #python3 & pip3 should be installed.
    $ pip3 install -r requirements.txt
    $ python3 main.py #To run in debug mode set debug=True in ./main.py

##### Note : 
1. REST Paradigm is used throughout the project.
2. All the related snapshots of working can be found in ./snapshots/*
