# eweive
<h1>Set-up instructions:</h1>

1. Have python installed on your computer
2. Create an environment for the project:

        # Linux
        sudo apt-get install python3-venv # If needed
        python3 -m venv .venv
        source .venv/bin/activate

        # macOS
        python3 -m venv .venv
        source .venv/bin/activate

        # Windows
        py -3 -m venv .venv
        .venv\scripts\activate

3. clone the repository 
4. In your terminal, run:

        % python
        
        >>> from app import db
        
        >>> db.createAll()
        
5. Hint: use the init_db.py file to create a superuser. 

        db_ex(
            '''
            INSERT INTO USERS(username, password, user_type, email, balance) VALUES("Superuser","superuser1234","SU", "su@gmail.com", 0)
            '''
        )
 
6. run the app using `python -m flask --debug run` for automatic refresh.
