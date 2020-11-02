from PyInquirer import prompt

#template forms that will be repeatedly used
#   type determines the type of input that it expects the user to perform
#   i.e. 'input' expects text while 'confirm' expect y/n
#   name is the key for the value that the user enters
#   message is the prompt that the form gives the user

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
        'choices': []
    }
]

_BADGE_MENU = [
    {
        'type' : 'list',
        'name' : 'badge',
        'message' : 'Give what badge?',
        'choices': []
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
    # returns one of the four choices from master menu (post, search, logout, quit)
    return prompt(_MASTER_MENU)['action']

def write_post():
    #user submits a title and a text body
    return prompt(_POST_FORM)

def edit_post(title, body):
    _EDIT_POST_FORM[0]['default'] = title
    _EDIT_POST_FORM[1]['default'] = body
    return prompt(_EDIT_POST_FORM)

def get_keyword():
    #gets multiple keywords with one query via regular expression
    #will require parsing
    return prompt(_KEYWORD_FORM)

def put_search_list(posts, empty):
    _SEARCH_FORM[0]['choices'] = [str(post) for post in posts] # updates the search_form to have the correct choices (posts)
    if not empty:
        _SEARCH_FORM[0]['choices'] += ['Next Page'] # if we have extra posts we're not showing, give option to go to next page
    return prompt(_SEARCH_FORM)['post']

def action_menu_select(show_priviledged_actions, show_answer_actions):
    #actions available for a searched post are dependent on 
    #the post and if user is privileged, so we'll build choices available here
    _ACTION_MENU[0]['choices'] = ['Upvote'] #anyone can upvote any post
    if not show_answer_actions:
        #if it's not an answer, it's a question and thus can be answered
        _ACTION_MENU['choices'].append('Post an answer')

    if show_priviledged_actions:
        #if user is privileged
        if show_answer_actions:
            #and it's an answer
            _ACTION_MENU['choices'].append('Mark as accepted answer') #can marks an answer as the answer
        #privileged users can give a badge, add a tag, or edit the post
        _ACTION_MENU['choices'].extend(
            [
                'Give a badge',
                'Add a tag',
                'Edit the post'
            ]
        )

    _ACTION_MENU['choices'].append("Return") #user can also choose to do nothing
    
    return prompt(_ACTION_MENU)['action']

def choose_badge(badge_list):
    #asks user to pick one badge name from all badge names
    _BADGE_MENU[0]['choices'] = badge_list
    return prompt(_BADGE_MENU)["badge"]

def request_tag():
    #returns any string as a tag
    return prompt(_TAG_FORM)['tag']
