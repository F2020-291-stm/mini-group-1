import cli
from database_access import Database

if __name__ == "__main__":
    database = Database()

    dbpath = cli.database_select()
    database.init_db(dbpath)
    session = None

    while True:
        if(session is None):
            if (cli.returning_user()):
                credentials = cli.login()
                session = database.verfiy_login(credentials[0], credentials[1])
                if (session is None):
                    print("Invalid Username or Password")
                else:
                    print("Logged in successfully")

            else:
                username = cli.register_username()
                info = cli.register_info()

                session = database.register(username, info['password'], info['name'], info['city'])

        else: 
    
    
        



