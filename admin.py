from sys import argv
from PyInquirer import prompt
from sqlite3 import connect

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
    """
    docstring
    """
    # Replace the user list
    USER_PROMPT[0]["choices"] = user_names
    return prompt(USER_PROMPT)["user"]

def choose_badge(badges):
    """
    docstring
    """
    # Replace the badge list
    REMOVE_BADGE_PROMPT[0]["choices"] = badges
    return prompt(REMOVE_BADGE_PROMPT)["badge"]

def choose_new_badge():
    return prompt(NEW_BADGE_PROMPT)


def get_privileged_users(database):
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
    database.execute(
        '''
        DELETE FROM badges
        WHERE bname = ?
        ''',
        (bname,)
    )

def add_badge(database, bname, btype):
    database.execute(
        '''
        INSERT INTO badges (bname, type)
        VALUES (?, ?)
        ''',
        (bname, btype)
    )

def add_privilege(database, uid):
    database.execute(
        '''
        INSERT INTO privileged (uid)
        VALUES (?)
        ''',
        (uid,)
    )

def remove_privilege(database, uid):
    database.execute(
        '''
        DELETE FROM privileged
        WHERE uid = ?
        ''',
        (uid,)
    )


if __name__ == "__main__":
    database = connect(argv[1], isolation_level=None)
    cursor = database.cursor()
    while True:
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
