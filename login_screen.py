import cli
import database
import sys

def login_screen(database):
    while True:
        # Check if the person logging in already has an account
        if (cli.returning_user()):
            # Ask for creditials and login
            credentials = cli.login()
            session = database.open_session(credentials[0], credentials[1])
            if session is not None:
                print("Logged in successfully")
                return session
            else:
                print("Invalid Username or Password")
                if(cli.quit_login()):
                    sys.exit(0)
        else:
            # Register 
            info = cli.register_info()
            session = database.register(info['username'], info['password'], info['name'], info['city'])
            if session is not None:
                print("Registered successfully")
                return session
            else:
                if(cli.quit_login()):
                    sys.exit(0)