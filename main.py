from database_access import Database
from login_screen import login_screen
from menu_screen import master_menu_screen
import subprocess
import sys
import cli

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install('PyInquirer')
    database = Database()
    #dbpath = cli.database_select()
    database.init_db('db/prj1.db')
    session = False
    while True:
        user = login_screen(database)
        login = True
        while login:
            login = master_menu_screen(user, database)



