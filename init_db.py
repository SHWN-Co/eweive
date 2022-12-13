import sqlite3

file = 'eweive2.db'

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
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
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
        highest_bid INTEGER NOT NULL,
       
        FOREIGN KEY(buyer_id) REFERENCES USERS (id),
        FOREIGN KEY(seller_id) REFERENCES USERS (id)

       ); """)

    db_ex("DROP TABLE IF EXISTS BID")
    db_ex("""CREATE TABLE IF NOT EXISTS BID(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        item_id INTEGER NOT NULL,
        highest_bid INTEGER NOT NULL,
        FOREIGN KEY(item_id) REFERENCES ITEMS (id)
        """)

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


    db_ex("DROP TABLE IF EXISTS ITEMS")
    db_ex("""CREATE TABLE IF NOT EXISTS ITEMS (
            id INTEGER PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            image TEXT NOT NULL, 
            key_words TEXT NOT NULL,
            seller_id INTEGER NOT NULL,
            time_limit TIME NOT NULL, 
            highest_bid INTEGER NOT NULL,
            FOREIGN KEY(seller_id) REFERENCES USERS (id)

        ); """) 

    db_ex("DROP TABLE IF EXISTS COMPLAINTS")
    db_ex("""CREATE TABLE IF NOT EXISTS COMPLAINTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER NOT NULL,
            complaint_cnt INTEGER NOT NULL, 
            reason TEXT NOT NULL, 
            FOREIGN KEY(user_id) REFERENCES USERS (id)
        ); """)

    db_ex("DROP TABLE IF EXISTS SUS_REPORTS")
    db_ex("""CREATE TABLE IF NOT EXISTS SUS_REPORTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            item_id INTEGER NOT NULL,
            FOREIGN KEY(item_id) REFERENCES ITEM (id)   
    ); """)
    
    db_ex("DROP TABLE IF EXISTS POLICE_REPORTS")
    db_ex("""CREATE TABLE IF NOT EXISTS POLICE_REPORTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            report_id INTEGER NOT NULL, 
            user_id INTEGER NOT NULL, 
            date_and_time DATETIME NOT NULL,
            item_id INTEGER NOT NULL, 
            FOREIGN KEY(report_id) REFERENCES SUS_REPORTS(id)
            FOREIGN KEY(user_id) REFERENCES USER(id) 
            FOREIGN KEY(item_id) REFERENCES ITEM(id)
        ); """)

    db_ex("DROP TABLE IF EXISTS USERS_ITEMS_BLOCKLIST")
    db_ex("""CREATE TABLE IF NOT EXISTS USERS_ITEMS_BLOCKLIST(
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES USER(id), 
            FOREIGN KEY(item_id) REFERENCES ITEM(id)
        ); """)


    # create first superuser
    db_ex('''
        INSERT INTO USERS(username, password, user_type, email) 
        VALUES('shwn', '173897', 'SU', 'sudevs@gmail.com')
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

    db_ex('''
        INSERT INTO ITEMS(id, title, image, key_words, seller_id, time_limit, highest_bid)
        VALUES('4356', 'Bose Speaker','ex image url', 'living room, sound system', '3849', '1:54:23', '320')
        ''')

    db_ex('''
        INSERT INTO COMPLAINTS(user_id, complaint_cnt, reason)
        VALUES('4522','1', 'too small' )
        ''')

# for i in range(6):
#     db_ex('''
#             INSERT INTO ITEMS(title, image, key_words, seller_id, highest_bid)
#             VALUES('TI-84 Plus CE Graphing Calculator','https://m.media-amazon.com/images/I/71yrLllDokL.jpg', 'calculator', '3','420');
#         ''')

# db_ex('''
#     UPDATE ITEMS 
#     SET description = "Electronically upgradeable graphing calculator allows you to have the most up-to-date functionality and software applications. Built-in MathPrint functionality allows you to input and view math symbols, formulas and stacked fractions exactly as they appear in textbooks. TI graph link offers increased capacity and speed. Advanced functions accessed through pull-down display menus. Horizontal and vertical split screen options. USB port for computer connectivity, unit-to-unit communication."
#     WHERE key_words = 'calculator'
#     ''')

# db_ex(
#     '''
#     INSERT INTO USERS(username, password, user_type, email, balance) VALUES("Superuser","superuser1234","SU", "su@gmail.com", 0)
#     '''
# )