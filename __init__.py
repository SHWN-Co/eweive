import sqlite3

file = 'eweive.db'

def db_ex(cmd):
    db = sqlite3.connect(file)
    c = db.cursor()
    out = c.execute(cmd)
    db.commit()
    db.close()
    return out

def db_setup():
    db_ex("DROP TABLE IF EXISTS USERS")
    db_ex("""CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY NOT NULL, 
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_number TEXT,
            cc_number TEXT,
            home_address TEXT
        ); """)
    # create first superuser
    db_ex('''
        INSERT INTO USERS(id, username, password, user_type, email) 
        VALUES('8685', 'shwn', '173897', 'SU', 'sudevs@gmail.com')
        ''')

db_setup()
