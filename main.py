import sys
from sys import argv

from menus import handle_login, handle_main_menu
from database import Database
import cli

if __name__ == "__main__":
    database = Database()
    try:
        #use given name for database
        database.init_db(argv[1])
    except IndexError:
        #if one not given, use default name
        database.init_db('db/prj1.db')
    while True:
        #logs in or registers user, and gets their session
        session = handle_login(database)
        while session.is_active():
            #keeps processing user-given main menu instructions
            #until the user logs out
            handle_main_menu(session, database)



