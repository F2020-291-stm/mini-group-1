import cli
import sys

from itertools import count

# SUBMENU
def handle_submenu(session, database, pid):
    """Once a user has searched for a post they can either post an answer
    to the post, or vote on the post. If the user is privileged they can also
    mark a post as the accepted answer, award a badge to user of the post, 
    add a tag to the post, or edit the post.

    Args:
        session (UserSession): Relevantly, contains uid of logged in user, and if user is privileged
        database (Database): The database. Necessary for all of these options
        pid (String): The pid of the post that's been selected
    """
    option = cli.action_menu_select(session.is_privileged(), database.is_answer(pid))
    if option == 'Post an answer': #post an answer to question pid
        post_answer(pid, session, database)
    elif option == 'Upvote': #upvote the post pid
        vote_post(pid, session, database)
    elif option == 'Mark as accepted answer': #mark pid as the accepted answer
        mark_accepted_answer(pid, database)
    elif option == 'Give a badge': #give badge to uid who posted pid
        give_badge(pid, database)
    elif option == 'Add a tag': #add a tag to pid
        add_tag(pid, database)
    elif option == 'Edit the post': #edits the contents of pid
        edit_post(pid, database)

def post_answer(qid, session, database):
    """Creates an answer post to a question post.

    Args:
        qid (String): The id of the question post
        session (UserSession): Relevantly, contains uid of logged in user
        database (Database): The database. Stores post in database
    """    
    answer = cli.write_post()
    database.post_answer(session, answer['title'], answer ['body'], qid)

def vote_post(pid, session, database):
    """Applies an upvote to specified post

    Args:
        pid (String): The id of the selected post
        session (UserSession): Relevantly ,contains uid of logged in user
        database (Database): The database. Stores vote in database
    """    
    success = database.vote_post(session, pid)
    if success: #voted was set to 1 if the user has already upvoted this post
        print('Vote Recorded')
    else: #otherwise, vote goes through
        print('Cannot Vote : Already Voted on Post')

def mark_accepted_answer(pid, database):
    """Sets pid to be the accepted answer. If the question already has an accepted answer
    User is prompted to override it and force pid to be the accepted answer instead.

    Args:
        pid (String): The id of the selected post
        database (Database): The database. Stores that pid is the accepted answer for qid
    """    
    if not database.mark_accepted_answer(pid): 
        if cli.force_mark_answer():
            database.mark_accepted_answer(pid, force=True)

def give_badge(pid, database):
    """Gives chosen badge to user of the selected post.

    Args:
        pid (String): The id of the selected post
        database (Database): The database. Updates user's badges
    """    
    badge_names = database.get_badge_list() #gets all badge names from database
    if len(badge_names) > 0:
        chosen_name = cli.choose_badge(badge_names) #gets user to pick one of them
        database.give_badge(pid, chosen_name) #then gives that badge to the user who wrote the post
    else:
        print("Sorry, there are no registered badges")

def add_tag(pid, database):
    """Prompts user for a tag and applies it to the post

    Args:
        pid (String): The id of the selected post
        database (Database): The database. Updates tags of a post
    """
    for tag in cli.request_tag():
        database.add_tag(pid, tag)

def edit_post(pid, database):
    """Prompts user to edit the body and title of selected post

    Args:
        pid (String): The id of the selected post
        database (Database): The database. Updates title/body of the post
    """    
    post = database.get_post(pid) #gets title and body of pid
    post = cli.edit_post(post[0], post[1]) #asks user to edit title and body of pid
    database.update_post(pid, post['title'], post['body'])

# LOGIN MENU
def handle_login(database):
    """Determines if user is returning or not. If they're returning, then 
    prompts user to log in. If not returning, prompts user to register.

    Args:
        database (Database): The database. Necessary for access of username/passwords or storage of new info

    Returns:
        UserSession: Creates and returns a session specific to the logged in user
    """    
    while True:
        # Check if the person logging in already has an account
        if (cli.returning_user()):
            # Ask for creditials and login
            credentials = cli.login()
            session = database.open_session(credentials[0], credentials[1])
            if session is not None:
                print("Logged in successfully")
                return session
            else:
                print("Invalid Username or Password")
                if(cli.quit_login()):
                    sys.exit(0)
        else:
            # Register 
            info = cli.register_info()
            session = database.register(info['username'], info['password'], info['name'], info['city'])
            if session is not None:
                print("Registered successfully")
                return session
            else:
                if(cli.quit_login()):
                    sys.exit(0)



# MAIN MENU
def handle_main_menu(session, database):
    """Prompts the user to choose between posting a question,
    searching for an existing post, logging out, or quitting the program.

    Args:
        session (UserSession): Relevantly, contains the uid of the logged in user
        database (Database): The database. Necessary for most of these options
    """    
    choice = cli.master_menu_select()
    if choice == 'Post a question':
        #user decides to post a question
        post_question_screen(session, database)
    elif choice == 'Search for posts':
        #user decides to select a post
        search_list = search_questions(database)
        if search_list is None:
            print('No matches')
        else:
            selected = False
            while not selected:
                answer = generate_search_list(search_list)
                if answer != '+':
                    selected = True
            #then selects what to do with it
            handle_submenu(session, database, answer)
    elif choice == 'Logout':
        #user logs out
        session.logout() #sets active to False, which halts the question loop and returns to logins screen
    else:
        #user quits. Code stops
        sys.exit(0)

def post_question_screen(session, database):
    """Prompts user to enter a title and body for their question.

    Args:
        session (UserSession): Relevantly, contains uid of logged in user
        database (Database): The database. Stores a post
    """    
    print("\nEnter your question\n")
    question = cli.write_post() #User enters title and body for question
    database.post_questions(session, question['title'], question['body']) #and it gets uploded to database
    
def search_questions(database):
    """Assembles posts that meet search criteria and prompts user
    to pick one of them. Shows user 5 posts at a time and allows user 
    to see more by replying with a next page request

    Args:
        database (Database): The database. Queries all posts

    Returns:
        [type]: [description]
    """    
    print("\nSearching the database....\n")
    keywords = cli.get_keyword()['keywords']
    keywords_list  = [string.strip() for string in keywords.split(';')]
    search_list = database.search_posts(keywords_list)
    return search_list
            
def generate_search_list(search_list): 
    empty = False
    try:
        items = []
        for _ in range(5):
            items.append(search_list.pop(0))
    except IndexError:
        empty = True
    if not search_list:
        empty = True
    return cli.put_search_list(items, empty)