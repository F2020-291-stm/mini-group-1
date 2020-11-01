import sqlite3
from datetime import date
from base64 import b64decode, b64encode
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
        self.db.create_function('INSTRNOCASE',2,_instr_nocase)
        self.cursor = self.db.cursor()
        if not exists:
            self.create_db()
    
    def create_db(self):
        with open('queries/prj-tables.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.executescript(sql_as_string)
        
    def sanitize(self, value):
        """
        Sanitizes values for database usage
        """
        pass

    def open_session(self, username, password):
        """
        Opens a session with the username and password
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
        if self.cursor.fetchone() is not None:
            self.cursor.execute(
            '''
            SELECT *
            FROM privileged
            WHERE uid = ?
            ''',
            (username,)
            )
            session = UserSession(username, privildeged=self.cursor.fetchone() is not None)
            session._activate()
            return session

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
        try:
            self.cursor.execute(
                '''
                INSERT INTO users(uid, name, pwd, city, crdate)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (username, name, password, city, date.today())
            )
            session = UserSession(username)
            session._activate()
            return session
        except sqlite3.IntegrityError:
            print("Error: Enter UNIQUE User ID")
    
    def post_questions(self, user, title, body):
        pid = self.generate_pid()
        self.cursor.execute(
            '''
            insert into posts(pid, pdate, title, body, poster)
            values (?,?,?,?,?)
            ''',
            (pid, date.today(), title, body, user)
        )
        self.cursor.execute(
            '''
            insert into questions(pid)
            values (?)
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
            INSERT INTO posts(pid, pdate, title, body, poster)
            VALUES (?,?,?,?,?) 
            ''',
            (pid, date.today(), title, body, user)
        )
        self.cursor.execute(
            '''
            INSERT INTO answers(pid, qid)
            VALUES (?,?)
            ''',
            (pid, qid)
        )
    
    def vote_post(self, user, pid):
        self.cursor.execute(
            '''
            SELECT *
            FROM votes
            WHERE pid = ?
            AND uid = ?
            ''',
            (pid, user)
        )
        if self.cursor.fetchone() is None:
            self.cursor.execute(
                '''
                SELECT max(vno)
                FROM votes   
                '''
            )
            vno = self.cursor.fetchone()[0]
            if vno is None:
                vno = 0
            else:
                vno = vno + 1            
            self.cursor.execute(
                '''
                INSERT INTO votes(pid, vno, vdate, uid)
                VALUES (?,?,?,?)
                ''',
                (pid, vno, date.today(), user)
            )
            return 0
        else:
            return 1
    
    def mark_accepted_answer(self, aid, force=False):
        self.cursor.execute(
            '''
            SELECT *
            FROM questions q, answers a
            WHERE a.pid = ?
            AND q.pid = a.qid
            AND q.theaid IS NOT NULL
            ''',
            (aid)
        )
        if (self.cursor.fetchone() is not None):
            return False
        
        self.cursor.execute(
            '''
            UPDATE questions
            SET theaid = ?
            WHERE pid = SOME (
                SELECT 
                FROM answers a
                WHERE a.pid = ?
            )
            ''',
            (aid, aid)
        )
        return True
    
    def get_badge_list(self):
        self.cursor.execute(
            '''
            SELECT bname
            FROM badges
            '''
        )
        return self.cursor.fetchall()

    def give_badge(self, pid, bname):
        try:
            self.cursor.execute(
                '''
                INSERT INTO ubadges
                VALUES (?, ?, ?)
                ''',
                (pid, date.today(), bname)
            )
        except sqlite3.IntegrityError:
            pass # Ignore because that just means the same badge has already been given today

    
    def generate_pid(self):
        self.cursor.execute(
            '''
            SELECT MAX(pid)
            FROM posts   
            '''
        )
        # TODO handle overflows and non-integer post ids
        pid = self.cursor.fetchone()[0]
        if pid is None:
            pid = str(0)
        else:
            pid = b64encode(int.from_bytes(b64decode((pid))), 'big' + 1)
        return pid

class UserSession:

    def __init__(self, uid, privildeged = False):
        self.uid = uid
        self.active = False
        self.privileged = privildeged

    def _activate(self):
        self.active = True

    def logout(self):
        self.active = False

    def is_active(self):
        return self.active

    def is_priviledged(self):
        return self.privileged

    def get_uid(self):
        return self.uid
        
    