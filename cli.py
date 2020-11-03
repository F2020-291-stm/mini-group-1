from PyInquirer import prompt, Separator

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
        'message': 'Tags (seperated by \';\')'
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
        'name': 'force',
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
    """Prompts user for a username and password.

    Returns:
        Tuple of strings: Username and password
    """    
    response = prompt(_LOGIN_FORM)
    return (response['username'], response['password'])

def register_info():
    """Prompts user for username, password, name and city name.

    Returns:
        Dictionary: Four strings - username, password, name, city name
    """    
    return prompt(_REGISTER_INFO_FORM)

def returning_user():
    """Asks user if they're a returning user.

    Returns:
        Boolean: Returns true if user is returning, false otherwise
    """   
    return prompt(_RETURNING_USER_FORM)['auth_type']

def quit_login():
    """Asks the user if they want to quit the program.

    Returns:
        Boolean: Returns true if user is quitting, false otherwise
    """    
    return prompt(_QUIT_FORM)['quit_or_continue']

def force_mark_answer():
    """Asks privileged user if they'd like to force an answer
    to become "the answer" for a specified question.

    Returns:
        Boolean: Returns true if user does want to force it, false otherwise
    """    
    return prompt(_FORCE_MARK_ANSWER_FORM)['force']

def database_select():
    """Asks for the name of the database to be used.

    Returns:
        String: Returns a string of the name (path) of the database to be used
    """    
    return prompt(_DATABASE_FORM)['database']

def master_menu_select():
    """User is prompted to select from the master menu: post, search, logout, or quit.

    Returns:
        String: Returns the string of the action chosen by the user
    """    
    return prompt(_MASTER_MENU)['action']

def write_post():
    """User is prompted to submit a title and a text body for a post.

    Returns:
        Dictionary: Returns a dictionary containing two strings - title and body
    """    
    #user submits a title and a text body
    return prompt(_POST_FORM)

def edit_post(title, body):
    """User is prompted to edit a title and body of a given post.

    Args:
        title (string): The current title (to be edited)
        body (string): The current body (to be edited)

    Returns:
        Dictionary: Returns a dictionary containing two strings - title and body
    """    
    _EDIT_POST_FORM[0]['default'] = title #updates _EDIT_POST_FORM such that it presents the current title and body
    _EDIT_POST_FORM[1]['default'] = body 
    return prompt(_EDIT_POST_FORM) #Then asks the user to edit it

def get_keyword():
    """Prompts user to submit as many key words as they like. User submits in a specified regular expression.

    Returns:
        Dictionary: Returns a dictionary containing a string of the regular expression containing the keyword(s)
    """    
    return prompt(_KEYWORD_FORM) #will require parsing when accessed

def put_search_list(posts, empty):
    """Shows user the first five posts that match their search. User can select a post or
    (if there are more than 5 results) select to move on to the next page.

    Args:
        posts (list): Contains all posts that match search criteria
        empty (boolean): Is true if we have 5 or less posts that match criteria

    Returns:
        Dictionary: Returns a dictionary containing the post that the user selected
    """
    display = [Separator("{:<5}|{:<10}|{:<30}|{:<40.40}|{:<15}|{:<5}|{:<5}".format('Pid', 'Date', 'Title', 'Body', 'Poster', 'Votes', 'Answers'))]
    for post in posts:
        item = {}
        if post[6] is not None:
            item['name'] = "{:<5}|{:<10}|{:<30}|{:<40.40}|{:<15}|{:<5}|{:<5}".format(post[0], post[1], post[2], post[3], post[4], post[5], post[6])
        else:
            item['name'] = "{:<5}|{:<10}|{:<30}|{:<40.40}|{:<15}|{:<5}".format(post[0], post[1], post[2], post[3], post[4], post[5])
        item['value'] = post[0]
        display.append(item)
    _SEARCH_FORM[0]['choices'] = display
    if not empty:
        _SEARCH_FORM[0]['choices'].append({'name':'Next Page', 'value': '+'})
    return prompt(_SEARCH_FORM)['post']

def action_menu_select(show_privileged_actions, show_answer_actions):
    """A user is looking at a post. This prompts the user to decide what 
    to do with the post.

    Args:
        show_priviledged_actions (boolean): Is true if the user is privileged
        show_answer_actions ([type]): Is true if the post being viewed is an answer

    Returns:
        Dictionary: Returns a dictionary containing a string of what option was selected
    """    
    #actions available for a searched post are dependent on 
    #the post and if user is privileged, so we'll build choices available here
    _ACTION_MENU[0]['choices'] = ['Upvote'] #anyone can upvote any post
    if not show_answer_actions:
        #if it's not an answer, it's a question and thus can be answered
        _ACTION_MENU[0]['choices'].append('Post an answer')
    
    if show_privileged_actions:
        #if user is privileged
        if show_answer_actions:
            #and it's an answer
            _ACTION_MENU[0]['choices'].append('Mark as accepted answer') #can marks an answer as the answer
        #privileged users can give a badge, add a tag, or edit the post
        _ACTION_MENU[0]['choices'].extend(
            [
                'Give a badge',
                'Add a tag',
                'Edit the post'
            ]
        )

    _ACTION_MENU[0]['choices'].append("Return") #user can also choose to do nothing
    
    return prompt(_ACTION_MENU)['action']

def choose_badge(badge_list):
    """Prompts user to pick one badge name among all the badge names

    Args:
        badge_list (list): A list containing strings of all the badge names

    Returns:
        String: Returns a string of the badge name
    """
    _BADGE_MENU[0]['choices'] = badge_list
    return prompt(_BADGE_MENU)["badge"]

def request_tag():
    """Prompts user to enter a tag that will be assigned to a post

    Returns:
        list(str): Returns a list of strings of the tags that was input
    """    
    tags = prompt(_TAG_FORM)['tag'].split(';')
    for i in range(len(tags)):
        tags[i] = tags[i].strip()
    return tags
