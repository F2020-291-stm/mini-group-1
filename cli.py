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
        'message': 'Are you a returning user',
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
        'type': 'input',
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
    return prompt(_AUTH_FORM)['auth_type']

def database_select():
    """
    docstring
    """
    return prompt(_DATABASE_FORM)['database']