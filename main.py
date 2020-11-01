import sys
from sys import argv

from menus import handle_login, handle_main_menu
from database import Database
import cli

if __name__ == "__main__":
    database = Database()
    database.init_db(argv[1])
    while True:
        session = handle_login(database)
        while session.is_active():
            handle_main_menu(session, database)



