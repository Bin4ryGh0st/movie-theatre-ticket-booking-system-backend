import os
import time
import hashlib

def generate_ticket_id():
    return hashlib.sha256(str(time.time()).encode()+os.urandom(16)).hexdigest()

def generate_show_id():
    return hashlib.md5(str(time.time()).encode()+os.urandom(16)).hexdigest()