import sqlite3

file = 'eweive.db'

def db_ex(cmd):
    db = sqlite3.connect(file)
    c = db.cursor()
    out = c.execute(cmd)
    db.commit()
    return out

def db_setup():
    db_ex("DROP TABLE IF EXISTS \"user\"")
    db_ex("DROP TABLE IF EXISTS \"transaction\"")
    db_ex("""CREATE TABLE IF NOT EXISTS  'user'(
        id INTEGER PRIMARY KEY NOT NULL,
        username VARCHAR,
        password VARCHAR,
        phone_number VARCHAR,
        cc_number VARCHAR,
        email VARCHAR);""")
    db_ex("""CREATE TABLE IF NOT EXISTS 'transaction'(
        id INTEGER PRIMARY KEY NOT NULL,
        transaction_number VARCHAR,
        buyer_id VARCHAR,
        seller_id, VARCHAR
        price VARCHAR,
        time TIMESTAMP);""")
