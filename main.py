import os
import time
import json
from core import setupdb,dbutils
from core.common import generate_show_id,generate_ticket_id
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/list/shows', methods=['GET'])
def list_shows():
    return (dbutil.list_shows())

@app.route('/book', methods=['POST'])
def book_ticket():
    try:
        user = request.json['user']
        contact = request.json['contact']
        show_id = request.json['show_id']
        show_time = request.json['show_time']
    except Exception as e:
        print("[Following exception has occcured]", e)
        return ({"Error":"Unknown Error Occured!"})
    return (dbutil.book_ticket(user, contact, show_id, show_time, generate_ticket_id()))

@app.route('/list/all/tickets/for/show/<show_id>', methods=['GET'])
def get_all_tickets_for_particular_show(show_id):
    try:
        return (dbutil.get_show_bookings(show_id))
    except Exception as e:
        print("[Following exception has occcured]", e)
        return ({"Error":"Unknown Error Occured!"})

@app.route('/detail/<ticket_id>', methods=['GET'])
def get_detail_from_ticket_id(ticket_id):
    try:
        return (dbutil.get_booking_details(ticket_id))
    except Exception as e:
        print("[Following exception has occcured]", e)
        return ({"Error":"Unknown Error Occured!"})

@app.route('/delete/ticket/<ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    try:
        return (dbutil.delete_ticket(ticket_id))
    except Exception as e:
        print("[Following exception has occcured]", e)
        return ({"Error":"Unknown Error Occured!"})

@app.route('/update/<ticket_id>/new/show/id/<new_show_id>', methods=['PUT'])
def update_given_ticket_time(ticket_id, new_show_id):
    try:
        print(ticket_id, new_show_id)
        return (dbutil.change_ticket_timing(ticket_id, new_show_id))
    except Exception as e:
        print("[Following exception has occcured]", e)
        return ({"Error":"Unknown Error Occured!"})

if __name__ == '__main__':
    if not os.path.exists("db.sqlite3"):
        '''Initializes Database instance if doesn't exists'''
        setupdb.init()
    else:
        pass
    
    dbutil = dbutils.dbutil()
    app.run(debug=False)
    




