import sqlite3
from datetime import date
from base64 import b64decode, b64encode
import os
import re
from string import ascii_lowercase, digits
from itertools import count

def _instr_nocase(X, Y):
    """[summary]

    Args:
        X ([type]): [description]
        Y ([type]): [description]

    Returns:
        [type]: [description]
    """    

    if X is None or Y is None:
        return 0
    if re.search(Y, X, re.IGNORECASE) is not None:
        return 1
    return 0
        

class Database:
    def init_db(self, path):
        """
        Initialize the database connection.

        Args:
            path (string): path that the chosen database lies in
        """
        exists = True
        if not os.path.exists(path):
            exists = False
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.create_function('INSTRNOCASE', 2, _instr_nocase)
        self.cursor = self.db.cursor()
        if not exists:
            self.create_db()
    
    def create_db(self):
        """Creates the database.
        """        
        with open('queries/prj-tables.sql') as sql_file:
            sql_as_string = sql_file.read()
            self.cursor.executescript(sql_as_string)
        
    def sanitize(self, value):
        """
        Sanitizes values for database usage.
        """
        pass

    def open_session(self, username, password):
        """Creates a session for this user.

        Args:
            username (String): A string containing the username
            password (String): A string containing the password

        Returns:
            [UserSesion]: A session containing uid and if the user is privileged or not
        """        
        self.cursor.execute( #finds all users with this username/password, either 0 or 1
            '''
            SELECT *
            FROM users
            WHERE uid = ?
            COLLATE NOCASE
            INTERSECT
            SELECT *
            FROM users
            WHERE pwd = ?
            ''',
            (username, password,)
        )
        if self.cursor.fetchone() is not None: #if the user exists then check if the user is privileged
            self.cursor.execute(
            '''
            SELECT *
            FROM privileged
            WHERE uid = ?
            COLLATE NOCASE
            ''',
            (username)
            )
            session = UserSession(username, privileged = self.cursor.fetchone() is not None) #creates a session for that user
            session._activate()
            return session

    def check_username(self, username):
        """Checks if username exists in the database.

        Args:
            username (String): A string containing the username

        Returns:
            Boolean: Returns 1 if the user exists, 0 if not
        """        
        self.cursor.execute(
            '''
            SELECT COUNT(*) > 0
            FROM users
            WHERE uid = ?
            COLLATE NOCASE
            ''',
            (username,)
        )
        return self.cursor.fetchone()

    def register(self, username, password, name, city):
        """Enters a user into the database. Initiates a session for this user
        If user already exists, then complains and doesn't allow it. 

        Args:
            username (String): A string containing the username
            password (String): A string containing the password
            name (String): A string containing the name
            city (String): A straining containing the city name

        Returns:
            [UserSession]: A session for the user created
        """        
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
        """Creates a post.

        Args:
            session (UserSession): A session for the user logged in
            title (String): Title of the post
            body (String): Body of the post
        """        
        pid = self.generate_pid() #generates a unique pid
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
        """Retrieves post with given pid.

        Args:
            pid (String): pid of the wanted post

        Returns:
            [Post]: The wanted post
        """        
        self.cursor.execute(
            '''
            SELECT title, body
            FROM posts
            WHERE pid = ?
            COLLATE NOCASE
            ''',
            (pid)
        )
        return self.cursor.fetchone()

    def update_post(self, pid, title, body):
        """Given a pid, updates its title and body with given parameters.

        Args:
            pid (String): pid of selected post
            title (String): String containing new title
            body (String): String containing new body
        """        
        self.cursor.execute( #finds pid and updates values
            '''
            UPDATE posts
            SET title = ?, body = ?
            WHERE pid = ? 
            ''',
            (title, body, pid,)
        )
    
    def search_posts(self, keyword_list):
        #TODO
        """[summary]

        Args:
            keyword (String): Given keyword for the search

        Returns:
            [type]: [description]
        """
        query = "SELECT p.pid AS pid\nFROM(\n"
        first = True
        for index in range(len(keyword_list)):
            keyword = keyword_list[index]
            if not first:
                query += "\nUNION ALL\n"
            else:
                first = False
            query +="SELECT p.pid AS pid, " + str(index) +" AS filter\nFROM posts p\nLEFT JOIN tags t\nON p.pid = t.pid \nWHERE (INSTRNOCASE(p.title,'"+ keyword +"') > 0\nOR INSTRNOCASE(p.body,'" + keyword + "') > 0\nOR INSTRNOCASE(t.tag,'" + keyword + "') > 0)"
        query +=") p\nGROUP BY pid\nORDER BY COUNT(*) DESC;"
        self.cursor.execute(query)
        return self.get_post_info(self.cursor.fetchall())
    
    def get_post_info(self, posts):
        if posts is None or not posts:
            return None
        query = ""
        for index in range(len(posts)):
            query += "SELECT *," + str(index) + " AS filter FROM posts WHERE pid =" + posts[index][0]
            if index != len(posts)-1:
                query += "\nUNION ALL\n"
        query+="\nORDER BY filter"
        with open('queries/search_posts.sql') as sql_file:
            sql_as_string = sql_file.read()
            sql_as_string = sql_as_string.replace('<placeholder>', query, 1)
        print(sql_as_string)
        self.cursor.execute(sql_as_string)
        return self.cursor.fetchall()
    
    def post_answer(self, session, title, body, qid):
        """Creates a post and assigns it as an answer to a chosen question.

        Args:
            session (UserSession): Relevantly, uid of answerer
            title (String): Title of answer
            body (String): Body of answer
            qid (String): pid of question being answered
        """        
        #creates a post and adds it to the posts and answers tables
        pid = self.generate_pid() #generates unique pid for new answer
        self.cursor.execute( #creates post
            '''
            INSERT INTO posts(pid, pdate, title, body, poster)
            VALUES (?,?,?,?,?) 
            ''',
            (pid, date.today(), title, body, session.get_uid())
        )
        self.cursor.execute( #assigns it as an answer to qid
            '''
            INSERT INTO answers(pid, qid)
            VALUES (?,?)
            ''',
            (pid, qid,)
        )
    
    def vote_post(self, session, pid):
        """Upvotes a selected post.

        Args:
            session (UserSession): Relevantly, uid of voter
            pid (String): pid of post being voted on

        Returns:
            Boolean: Returns 0 upon successful vote, 1 if user has already cast a vote on that post
        """        
        self.cursor.execute( #finds all votes on pid made by user of the session
            '''
            SELECT *
            FROM votes
            WHERE pid = ?
            AND uid = ?
            COLLATE NOCASE
            ''',
            (pid, session.get_uid(),)
        )
        if self.cursor.fetchone() is None:
            #if there are none, that means this user has not voted
            #on this post yet, which means they now can
            self.cursor.execute(
                '''
                SELECT max(vno)
                FROM votes   
                '''
            )
            #set vno of this new vote to the biggest vno+1
            vno = self.cursor.fetchone()[0]
            if vno is None:
                vno = 0
            else:
                vno = vno + 1
            #and now apply this vote to the database          
            self.cursor.execute(
                '''
                INSERT INTO votes(pid, vno, vdate, uid)
                VALUES (?,?,?,?)
                ''',
                (pid, vno, date.today(), session.get_uid(),)
            )
            return 0 #upon successful vote, return 0
        else:
            return 1 #upon unsuccessful vote, return 1
    
    def mark_accepted_answer(self, aid, force=False):
        """Marks an answer as the accepted answer to a post. User
        can choose if they'd like to override any current accepted answers
        with this one.

        Args:
            aid (String): pid of answer being chosen as the accepted answer
            force (bool, optional): True if user wants to override any current accepted answers.
                 Defaults to False.

        Returns:
            Boolean: Returns true if post was assigned as accepted answer, false if it wasn't
        """        
        self.cursor.execute( #finds the question and checks if it is already answered
            '''
            SELECT *
            FROM questions q, answers a
            WHERE a.pid = ?
            AND q.pid = a.qid
            AND q.theaid IS NOT NULL
            ''',
            (aid,)
        )
        if (not force and self.cursor.fetchone() is not None):
            #if the question already has a "the answer", then this answer cannot become
            #the accepted answer, so return false. This step is overriden if force is set to true
            return False
        #otherwise, set this answer to be "the answer"
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
            (aid, aid,)
        )
        return True #return true to signify that it went through
    
    def get_badge_list(self):
        """Finds the name of all badges.

        Returns:
            List: list of all badge names
        """        
        #returns list of all badge names
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
        """Gives a chosen badge to the poster of a post.

        Args:
            pid (String): pid of chosen post
            bname (String): name of chosen badge
        """        
        self.cursor.execute( #gets uid of poster
            '''
            Select poster
            From posts
            Where pid = ?
            ''',
            (pid)
        )
        uid = self.cursor.fetchone()

        #gives badge bname to user uid, right now
        try:
            self.cursor.execute(
                '''
                INSERT INTO ubadges
                VALUES (?, ?, ?)
                ''',
                (pid, date.today(), bname,)
            )
        except sqlite3.IntegrityError:
            pass # Ignore because that just means the same badge has already been given today

    def add_tag(self, pid, tag):
        """Adds a tag to a specified post. If post already has that tag, then
        don't add it again.

        Args:
            pid (String): pid of select posted
            tag (String): string containing the chosen tag

        Returns:
            Boolean: Return 0 to signify a successful addition of a tag, 1 otherwise
        """        
        self.cursor.execute( #checks if this tag is already applied to pid
            '''
            SELECT *
            FROM tags
            WHERE tag = ?
            COLLATE NOCASE
            ''',
            (tag,)
        )
        if (self.cursor.fetchone() is None):
            #if it hasn't been tagged with this tag, then tag it
            self.cursor.execute(
                '''
                INSERT INTO tags
                VALUES (?, ?)
                ''',
                (pid, tag,)
            )
            return 0 #return a 0 to signify a success
        
        return 1 #otherwise do nothing and return 1 to signify a failure

    
    def generate_pid(self):
        """Gerenerates a unique pid

        Returns:
            String: The generated pid
        """        
        self.cursor.execute(
            '''
            SELECT MAX(pid) + 1
            FROM posts   
            '''
        )
        # TODO handle overflows and non-integer post ids
        pid = self.cursor.fetchone()[0]
        if pid is None:
            pid = str(0)
        # else:
        #     pid = b64encode(int.from_bytes(b64decode((pid))), 'big' + 1)
        return pid
    

    def is_answer(self, pid):
        """Given a pid, checks if it is an answer (as opposed to a question)

        Args:
            pid (String): pid of potential answer

        Returns:
            Boolean: Return True if it is an answer, False otherwise
        """        
        self.cursor.execute(
            '''
            SELECT *
            FROM answers
            WHERE pid = ?
            ''',
            (pid,)
        )
        if self.cursor.fetchone() is not None:
            return True
        return False

class UserSession:
    """Used to keep track of which user is logged in such that their actions
    Can be attributed to their uid
    """    

    def __init__(self, uid, privileged = False):
        #uid is the user id of the user that this session corresponds to
        #Once a session has began, main.py will repeatedly allow the user
        #   to select options from a menu until they logout. Active determines
        #   whether a user is logged our or not
        #privileged sessions have more options available to them for 
        #   interacting with other user's posts
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
        
def get_next_lex(string1):
    string = string1.lower()
    done = False
    lex_order = ascii_lowercase + digits
    if string is None or len(string) == 0:
        return lex_order[0]
    for index in range(len(string) - 1, -1, -1):
        if string[index] != lex_order[-1]:
            done = True
            break
    if not done:
        return string + lex_order[0]
    for index1 in range(len(lex_order)):
        if string[index] == lex_order[index1]:
            return string[:index]+lex_order[index1+1]+string[index + 1:]    