import sqlite3
from datetime import date
import os

class Database:
    db = None
    cursor = None

    def init_db(self, path):
        """
        Initialize the database connection
        """
        exists = True
        if not os.path.exists(path):
            exists = False
        self.db = sqlite3.connect(path, isolation_level=None)
        self.cursor = self.db.cursor()
        if not exists:
            self.create_db()

    def create_db(self):
        with open('db/prj-tables.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.executescript(sql_as_string)
        
    def sanitize(self, value):
        """
        Sanitizes values for database usage
        """
        pass

    def verify_login(self, username, password):
        """
        Verifies a username and password
        """
        self.cursor.execute(
            '''
            SELECT *
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
        done = True
        try:
            self.cursor.execute(
                '''
                INSERT INTO users VALUES (?, ?, ?, ?, ?)
                ''',
                (username, name, password, city, date.today())
            )
        except sqlite3.IntegrityError:
            print("Error: Enter UNIQUE User ID")
            done = False
        return done
    
    def post_questions(self, user, title, body):
        with open('queries/post_question.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.execute(
            sql_as_string,
            (date.today(), title, body, user)
        )
    
    def search_posts(self, keyword):
        with open('queries/search_posts.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.execute(
            sql_as_string,
            (keyword, keyword, keyword) #keyword
            )
        return self.cursor.fetchall()
        