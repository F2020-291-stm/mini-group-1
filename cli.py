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

_TAG_FORM = [
    {
        'type': 'input',
        'name': 'tag',
        'message': 'Tag'
    },
]

_REGISTER_INFO_FORM = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Username'
    },
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
        'name' : 'action',
        'message' : 'What do you want to do?',
        'choices': [
            'Post a question',
            'Search for posts',
            'Logout',
            'Quit'
        ]
    }
]

_FORCE_MARK_ANSWER_FORM = [
    {
        'type': 'confirm',
        'name': 'force_overwrite',
        'message': 'Question already has an accepted answer, do you want to overwrite?',
        'default' : False
    }
]

_POST_FORM = [
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

_EDIT_POST_FORM = [
    {
        'type' : 'input',
        'name' : 'title',
        'message' : 'title',
        'default' : ''
    },    
    {
        'type' : 'input',
        'name' : 'body',
        'message' : 'body',
        'default' : ''
    }
]

_KEYWORD_FORM = [
    {
        'type' : 'input',
        'name' : 'keywords',
        'message' : 'Enter Search Keywords seperated by \';\'\n'
    }
]

_SEARCH_FORM = [
    {
        'type' : 'list',
        'name' : 'post',
        'message' : 'Select a post',
        'choices' : None
    }
]

_ACTION_MENU = [
    {
        'type' : 'list',
        'name' : 'action',
        'message' : 'What do you want to do?',
        'choices': [
            'Post an answer',
            'Vote on post',
            'Accept the answer',
            
        ]
    }
]

def login():
    """
    docstring
    """
    response = prompt(_LOGIN_FORM)
    return (response['username'], response['password'])

def register_info():
    return prompt(_REGISTER_INFO_FORM)

def returning_user():
    """
    docstring
    """
    return prompt(_RETURNING_USER_FORM)['auth_type']

def quit_login():
    return prompt(_QUIT_FORM)['quit_or_continue']

def force_mark_answer():
    return prompt(_FORCE_MARK_ANSWER_FORM)['force']

def database_select():
    """
    docstring
    """
    return prompt(_DATABASE_FORM)['database']

def master_menu_select():
    return prompt(_MASTER_MENU)['action']

def write_post():
    return prompt(_POST_FORM)

def edit_post(title, body):
    _EDIT_POST_FORM[0]['default'] = title
    _EDIT_POST_FORM[1]['default'] = body
    return prompt(_EDIT_POST_FORM)

def get_keyword():
    return prompt(_KEYWORD_FORM)

def put_search_list(posts, empty):
    _SEARCH_FORM[0]['choices'] = [str(post) for post in posts]
    if not empty:
        _SEARCH_FORM[0]['choices'] += ['Next Page']
    return prompt(_SEARCH_FORM)['post']

def action_menu_select(show_priviledged_actions, show_answer_actions):
    # Cannot store this as a "constant" as we edit it here
    menu = {
        'type' : 'list',
        'name' : 'action',
        'message' : 'What do you want to do?',
        'choices': [
            'Upvote'
        ]
    }
    if not show_answer_actions:
        menu['choices'].append('Post an answer')

    if show_priviledged_actions:
        if show_answer_actions:
            menu['choices'].append('Mark as accepted answer')
        menu['choices'].extend(
            [
                'Give a badge',
                'Add a tag',
                'Edit the post'
            ]
        )

    menu['choices'].append("Return")
    
    return prompt([menu])['action']

def choose_badge(badge_list):
    badge_menu = {
        'type' : 'list',
        'name' : 'badge',
        'message' : 'Give what badge?',
        'choices': badge_list
    }
    return prompt([badge_menu])["badge"]

def request_tag():
    return prompt(_TAG_FORM)['tag']
