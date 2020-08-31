# Movie Theatre Ticket Booking System Backend
---
### Zomentum Hiring Challenge (Backend)

##### Functionality :
> 1. Endpoint for booking movie ticket for available shows.
<br>
> POST /book
<br>
> 2. Endpoint to update ticket timings.
<br>
> PUT /update/<ticket_id>/new/show/id/<new_show_id>
<br>
> 3. Endpoint to view all tickets for particular show.
<br>
> GET /list/all/tickets/for/show/<show_id>
<br>
> 4. Endpoint to delete particular ticket.
<br>
> DELETE /delete/ticket/<ticket_id>
<br>
> 5. Endpoint to view the user’s details based on the ticket id.
<br>
> GET /detail/<ticket_id>
<br>
> 6. Deletes expired shows/tickets from database using following techniques : 
<br>
> a. Lazy update : Triggers refining of database after every 10th(Variable) request to it.
<br>
> b. Scheduler : A parallel thread which triggers refining of database after every 8 hours(variable).
<br>
> c. ON DELETE CASCADE in database while creating schema which deletes all the expired tickets if the show is deleted itself using following query :
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
##### Techstack Used :
> 1. Python3
> 3. Flask Microframework for creating WEB APIs.
> 2. SQLite3 for data storage and manupulation purposes.

##### Setup Procedure:
    $ #python3 & pip3 should be installed.
    $ pip3 install -r requirements.txt
    $ python3 main.py #To run in debug mode set debug=True in ./main.py

###### Note : 
> 1. REST Paradigm is used throughout the project.
> 2. All the related snapshots of working can be found in ./snapshots/*
