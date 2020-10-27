import cli
from database_access import Database
from login_screen import login_screen


if __name__ == "__main__":
    database = Database()
    #dbpath = cli.database_select()
    database.init_db('db/m-prj1.db')
    session = False
    login_screen(session, database)



