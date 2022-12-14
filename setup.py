import sqlite3
from app import db

def db_create():
    db.create_all()

def db_ex(cmd):
    file = 'eweivenew.db'
    db = sqlite3.connect(file)
    c = db.cursor()
    out = c.execute(cmd)
    db.commit()
    db.close()
    return out

#function to return balance
def returnBalance(balance):
    a = 0
    if balance is not None:
        a = balance/100
    return a

def db_run():
    db_create()
    db_ex('''
        INSERT INTO USERS(username, password, user_type, email, balance)    
        SELECT "Superuser","superuser1234","SU", "su@gmail.com", 0
        WHERE NOT EXISTS (SELECT * FROM USERS)
        ''')