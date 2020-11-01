import sys
from sys import argv

from menus import handle_login, handle_main_menu
from database import Database
import cli

if __name__ == "__main__":
    database = Database()
    try:
        database.init_db(argv[1])
    except IndexError:
        database.init_db('db/prj1.db')
    while True:
        session = handle_login(database)
        while session.is_active():
            handle_main_menu(session, database)



