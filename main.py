import cli
from database_access import Database
from login_screen import login_screen
from menu_screen import master_menu_screen


if __name__ == "__main__":
    database = Database()
    #dbpath = cli.database_select()
    database.init_db('db/prj1.db')
    session = False
    while True:
        user = login_screen(database)
        login = True
        while login:
            login = master_menu_screen(user, database)



