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
    
    db_ex("DROP TABLE IF EXISTS TRANSACTIONS")    
    db_ex("""CREATE TABLE IF NOT EXISTS TRANSACTIONS (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date_and_time DATETIME NOT NULL,
        item_id INTEGER NOT NULL,
        buyer_id INTEGER NOT NULL UNIQUE,
        seller_id INTEGER NOT NULL UNIQUE, 
        highest_bid INTEGER NOT NULL
       
        FOREIGN KEY(buyer_id) REFERENCES USERS (id)
        FOREIGN KEY(seller_id) REFERENCES USERS (id)
       ); """)
#figure out why foreign key is running into trouble ^
    db_ex("DROP TABLE IF EXISTS OU_APPLICATION")    
    db_ex("""CREATE TABLE IF NOT EXISTS OU_APPLICATIONS (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        status VARCHAR(255) NOT NULL,
        app_id INTEGER NOT NULL,
        user_type VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        annual_income INTEGER NOT NULL
       ); """)  
     

    # create first superuser
    db_ex('''
        INSERT INTO USERS(id, username, password, user_type, email) 
        VALUES('8685', 'shwn', '173897', 'SU', 'sudevs@gmail.com')
        ''')
    
    # add first item transaction
    db_ex('''
    INSERT INTO TRANSACTIONS(date_and_time, item_id, buyer_id, seller_id, highest_bid)
    VALUES('2022-12-03 12:45:34', '5556', '8790', '3345', '56')
    ''')
    db_ex('''
    INSERT INTO TRANSACTIONS(date_and_time, item_id, buyer_id, seller_id, highest_bid)
    VALUES('2022-12-04 1:30:09', '8834', '7329', '1123', '310')
    ''')

    db_ex('''
    INSERT INTO OU_APPLICATIONS(status, app_id, user_type, first_name, last_name, email, password, annual_income)
    VALUES('pending', '112', 'GUEST USER', 'JIE', 'WIE', 'jwei@cuny.com','secur!ty', '1000000')
    ''')


db_setup()