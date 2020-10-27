from PyInquirer import prompt

_DATABASE_FORM = [
    {
        'type': 'input',
        'name': 'database',
        'message': 'Database Location'
    },
]

_RETURNING_USER_FORM = [
    {
        'type': 'confirm',
        'name': 'auth_type',
        'message': 'Are you a returning user?',
        'default': True
    }
]

_LOGIN_FORM = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Username'
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Password'
    }
]

_REGISTER_USERNAME_FORM = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Username'
    }
]

_REGISTER_INFO_FORM = [
    {
        'type': 'password',
        'name': 'password',
        'validate': True,
        'message': 'Password'
    },
    {
        'type': 'input',
        'name': 'name',
        'message': 'Name'
    },
    {
        'type': 'input',
        'name': 'city',
        'message': 'City'
    }
]

_QUIT_FORM = [
    {
        'type': 'confirm',
        'name': 'quit_or_continue',
        'message': 'Do you want to quit?',
        'default' : False
    }
]

_MASTER_MENU =[
    {
        'type' : 'list',
        'name' : 'master menu',
        'message' : 'What do you want to do?',
        'choices': [
            'Post a question',
            'Search for posts',
            'Logout',
            'Quit'
        ]
    }
]

_POST_QUESTION = [
    {
        'type' : 'input',
        'name' : 'title',
        'message' : 'title'
    },    
    {
        'type' : 'input',
        'name' : 'body',
        'message' : 'body'
    }
]

def login():
    """
    docstring
    """
    response = prompt(_LOGIN_FORM)
    return (response['username'], response['password'])

def register_username():
    return prompt(_REGISTER_USERNAME_FORM)['username']

def register_info():
    return prompt(_REGISTER_INFO_FORM)

def returning_user():
    """
    docstring
    """
    return prompt(_RETURNING_USER_FORM)['auth_type']

def quit_login():
    return prompt(_QUIT_FORM)['quit_or_continue']

def database_select():
    """
    docstring
    """
    return prompt(_DATABASE_FORM)['database']

def master_menu_select():
    return prompt(_MASTER_MENU)

def post_question():
    return prompt(_POST_QUESTION)