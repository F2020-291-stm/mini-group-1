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
            session = UserSession(username, priviledged=self.cursor.fetchone() is not None)
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
    
    def post_questions(self, session, title, body):
        pid = self.generate_pid()
        self.cursor.execute(
            '''
            insert into posts(pid, pdate, title, body, poster)
            values (?,?,?,?,?)
            ''',
            (pid, date.today(), title, body, session.get_uid())
        )
        self.cursor.execute(
            '''
            insert into questions(pid)
            values (?)
            ''', 
            (pid,)
        )

    def get_post(self, pid):
        self.cursor.execute(
            '''
            SELECT title, body
            FROM posts
            WHERE pid = ?
            ''',
            (pid,)
        )
        return self.cursor.fetchone()

    def update_post(self, pid, title, body):
        self.cursor.execute(
            '''
            UPDATE posts
            SET title = ?, body = ?
            WHERE pid = ? 
            ''',
            (title, body, pid)
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
        
    def post_answer(self, session, title, body, qid):
        pid = self.generate_pid()
        self.cursor.execute(
            '''
            INSERT INTO posts(pid, pdate, title, body, poster)
            VALUES (?,?,?,?,?) 
            ''',
            (pid, date.today(), title, body, session.get_uid())
        )
        self.cursor.execute(
            '''
            INSERT INTO answers(pid, qid)
            VALUES (?,?)
            ''',
            (pid, qid)
        )
    
    def vote_post(self, session, pid):
        self.cursor.execute(
            '''
            SELECT *
            FROM votes
            WHERE pid = ?
            AND uid = ?
            ''',
            (pid, session.get_uid())
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
                (pid, vno, date.today(), session.get_uid())
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
        badges = []
        for entry in self.cursor.fetchall():
            badges.append(entry[0])
        return badges

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

    def add_tag(self, pid, tag):
        self.cursor.execute(
            '''
            SELECT *
            FROM tags
            WHERE INSTRNOCASE(tag, ?)
            ''',
            (tag,)
        )
        if (self.cursor.fetchone() is None):
            self.cursor.execute(
                '''
                INSERT INTO tags
                VALUES (?, ?)
                ''',
                (pid, tag)
            )

    
    def generate_pid(self):
        self.cursor.execute(
            '''
            SELECT MAX(pid) + 1
            FROM posts   
            '''
        )
        # TODO handle overflows and non-integer post ids
        pid = self.cursor.fetchone()[0]
        # if pid is None:
        #     pid = str(0)
        # else:
        #     pid = b64encode(int.from_bytes(b64decode((pid))), 'big' + 1)
        return pid

class UserSession:

    def __init__(self, uid, privileged = False):
        self.uid = uid
        self.active = False
        self.privileged = privileged

    def _activate(self):
        self.active = True

    def logout(self):
        self.active = False

    def is_active(self):
        return self.active

    def is_privileged(self):
        return self.privileged

    def get_uid(self):
        return self.uid
        
    