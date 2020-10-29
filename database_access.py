import sqlite3
from datetime import date
import os
import re

def _instr_nocase(X, Y):
    if re.search(Y, X, re.IGNORECASE) is not None:
        return 1
    return 0

class Database:
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
        pid = self.generate_pid()
        self.cursor.execute(
        '''
        insert into posts(pid, pdate, title, body, poster)
        values(
            ?,?,?,?,?
        )
        ''',
        (pid, date.today(), title, body, user)
        )
        self.cursor.execute(
        '''
        insert into questions(pid)
        values(
            ?
        )
        ''', 
        (pid)
        )
    
    def search_posts(self, keyword):
        self.db.create_function('INSTRNOCASE',2,_instr_nocase)
        with open('queries/search_posts.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.execute(
            sql_as_string,
            (keyword, keyword, keyword) #keyword
            )
        return self.cursor.fetchall()
        
    def post_answers(self, user, title, body, qid):
        pid = self.generate_pid()
        self.cursor.execute(
            '''
            insert into posts(pid, pdate, title, body, poster)
            values(
            ?,?,?,?,?
            ) 
            ''',
            (pid, date.today(), title, body, user)
        )
        self.cursor.execute(
            '''
            insert into answers(pid, qid)
            values(
                ?,?
            )
            ''',
            (pid, qid)
        )
    
    def vote_post(self, user, pid):
        self.cursor.execute(
            '''
                select *
                from votes
                where pid = ?
                and uid = ?
            ''',
            (pid, user)
        )
        if self.cursor.fetchone() is None:
            self.cursor.execute(
            '''
                select max(vno)
                from votes   
            '''
            )
            vno = self.cursor.fetchone()[0]
            if vno is None:
                vno = str(1)
            else:
                vno = str(int(vno) + 1)            
            self.cursor.execute(
            '''
            insert into votes(pid, vno, vdate, uid)
            values(
            ?,?,?,?
            )
            ''',
            (pid, vno, date.today(), user)
            )
            return 0
        else:
            return 1
    
    def generate_pid(self):
        self.cursor.execute(
            '''
                select max(pid)
                from posts   
            '''
        )
        pid = self.cursor.fetchone()[0]
        if pid is None:
            pid = str(1)
        else:
            pid = str(int(pid) + 1)
        return pid