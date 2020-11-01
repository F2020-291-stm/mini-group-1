from sys import argv

from database import Database
from login_screen import login_screen
from menu_screen import master_menu_screen
import cli

if __name__ == "__main__":
    database = Database()
    database.init_db(argv[1])
    while True:
        session = login_screen(database)
        while session.is_active():
            master_menu_screen(session, database)



