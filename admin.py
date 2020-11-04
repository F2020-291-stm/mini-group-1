from sys import argv
from PyInquirer import prompt
from sqlite3 import connect
from os.path import exists

ACTION_PROMPT = [
    {
        "type": "list",
        "name": "action",
        "message": "What action do you want to do",
        "choices": [
            "Add Privileged User",
            "Remove Privileged User",
            "Add Badge",
            "Remove Badge",
            "Exit"
        ]
    }
]

USER_PROMPT = [
    {
        "type": "list",
        "name": "user",
        "message": "Select a user",
        "choices": []
    }
]

REMOVE_BADGE_PROMPT = [
    {
        "type": "list",
        "name": "badge",
        "message": "Select a user",
        "choices": []
    }
]

NEW_BADGE_PROMPT = [
    {
        "type": "input",
        "name": "name",
        "message": "Name for badge",
    },
    {
        "type": "list",
        "name": "type",
        "message": "What is the badge type",
        "choices": [
            "gold",
            "silver",
            "bronze"
        ]
    }   
]



def choose_user(user_names):
    """ Prompt the user to choose a username
    """
    # Replace the user list
    USER_PROMPT[0]["choices"] = user_names
    return prompt(USER_PROMPT)["user"]

def choose_badge(badges):
    """ Prompt the user to choose a badge name
    """
    # Replace the badge list
    REMOVE_BADGE_PROMPT[0]["choices"] = badges
    return prompt(REMOVE_BADGE_PROMPT)["badge"]

def choose_new_badge():
    """ Prompt the user to create a new badge name
    """
    return prompt(NEW_BADGE_PROMPT)


def get_privileged_users(database):
    """ Get all privileged users from the database
    """
    database.execute(
        '''
        SELECT u.uid
        FROM users u, privileged p
        WHERE p.uid = u.uid
        '''
    )
    users = []
    for entry in database.fetchall():
        users.append(entry[0])
    return users

def get_non_privileged_users(database):
    """ Get all non prvileged users from the database
    """
    database.execute(
        '''
        SELECT uid
        FROM users

        EXCEPT

        SELECT uid
        FROM privileged
        '''
    )
    users = []
    for entry in database.fetchall():
        users.append(entry[0])
    return users

def get_badges(database):
    """ Get all badges
    """
    database.execute(
        '''
        SELECT bname
        FROM badges
        '''
    )
    badges = []
    for entry in database.fetchall():
        badges.append(entry[0])
    return badges

def remove_badge(database, bname):
    """ Remove a badge from the database
    """
    database.execute(
        '''
        DELETE FROM badges
        WHERE bname = ?
        ''',
        (bname,)
    )

def add_badge(database, bname, btype):
    """ Add a badge to the database
    """
    database.execute(
        '''
        INSERT INTO badges (bname, type)
        VALUES (?, ?)
        ''',
        (bname, btype)
    )

def add_privilege(database, uid):
    """ Add a user to the privileged list
    """
    database.execute(
        '''
        INSERT INTO privileged (uid)
        VALUES (?)
        ''',
        (uid,)
    )

def remove_privilege(database, uid):
    """ Remove a user from the privileged list
    """
    database.execute(
        '''
        DELETE FROM privileged
        WHERE uid = ?
        ''',
        (uid,)
    )


if __name__ == "__main__":
    # Init database connection (set to auto commit)
    if not exists(argv[1]):
        print("Database is not initialized yet, run main.py first before using admin panel")
        exit(1)
    database = connect(argv[1], isolation_level=None)
    cursor = database.cursor()
    while True:
        # Primpt the user for an action and handle the appropriate action
        action = prompt(ACTION_PROMPT)["action"]
        if (action == "Add Privileged User"):
            uid = choose_user(get_non_privileged_users(cursor))
            add_privilege(cursor, uid)
        elif (action == "Remove Privileged User"):
            uid = choose_user(get_privileged_users(cursor))
            remove_privilege(cursor, uid)
        elif (action == "Add Badge"):
            badge_info = choose_new_badge()
            add_badge(cursor, badge_info["name"], badge_info["type"])
        elif (action == "Remove Badge"):
            badge = choose_badge(get_badges(cursor))
            remove_badge(cursor, badge)
        elif (action == "Exit"):
            exit() 
