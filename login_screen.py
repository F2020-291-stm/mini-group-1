import cli
import database_access
import sys

def login_screen(database):
    done = False
    while not done:
        if (cli.returning_user()):
            credentials = cli.login()
            session = False
            if database.verify_login(credentials[0], credentials[1]) is not None:
                session = True
            if session:
                print("Logged in successfully")
                return credentials[0]
            else:
                print("Invalid Username or Password")
                if(cli.quit_login()):
                    sys.exit(0)
        else:
            username = cli.register_username()
            info = cli.register_info()
            if database.register(username, info['password'], info['name'], info['city']):
                print("Registered successfully")
                return username
            else:
                if(cli.quit_login()):
                    sys.exit(0)