import sqlite3
from datetime import date

class Database:
    db = None
    cursor = None

    def init_db(self, path):
        """
        Initialize the database connection
        """
        self.db = sqlite3.connect(path)
        self.cursor = db.cursor()

    def sanitize(self, value):
        """
        Sanitizes values for database usage
        """
        pass

    def verfiy_login(self, username, password):
        """
        Verifies a username and password
        """
        self.cursor.execute(
            '''
            SELECT COUNT(*) > 0
            FROM users
            WHERE uid = ?
            AND pwd = ?
            ''',
            (username, password)
        )
        return self.cursor.fetchone()

    def check_username(self, username):
        self.cursor.execute(
            '''
            SELECT COUNT(*) > 0
            FROM users
            WHERE uid = ?
            ''',
            (username)
        )
        return self.cursor.fetchone()

    def register(self, username, password, name, city):
        self.cursor.execute(
            '''
            INSERT INTO users VALUES (?, ?, ?, ?, ?)
            ''',
            (username, name, password, city, date.today())
        )
