import cli
import sys

from util import PQ
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
    elif option == 'Vote on post': #upvote the post pid
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
    voted = database.vote_post(session, pid)
    if voted: #voted was set to 1 if the user has already upvoted this post
        print('Cannot Vote : Already Voted on Post')
    else: #otherwise, vote goes through
        print('Vote Recorded')

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
    chosen_name = cli.choose_badge(badge_names) #gets user to pick one of them
    database.give_badge(pid, chosen_name) #then gives that badge to the user who wrote the post

def add_tag(pid, database):
    """Prompts user for a tag and applies it to the post

    Args:
        pid (String): The id of the selected post
        database (Database): The database. Updates tags of a post
    """    
    tagged = database.add_tag(pid, cli.request_tag())
    if tagged: #tagged gets set to 1 if the post already has this tag
        print('Tag Already Applied')
    else: #otherwise it goes through
        print('Tag Recorded')

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
        pid = search_questions(database)
        if pid is not None:
            pid = str(pid)
            #then selects what to do with it
            handle_submenu(session, database, pid)
        else:
            print('No matches')
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
    keywords = cli.get_keyword()['keywords'] # get multiple keywords in a regular expression
    keywords_list  = [string.strip() for string in keywords.split(';')] # parse regular expression
    ordered_posts = PQ() # convert dict to PQ
    for keyword in keywords_list:
        posts = database.search_posts(keyword) #finds posts with that keyword in title, body, or tags
        for post in posts:
            if ordered_posts.check_if_in_queue(post):
                #for posts that appear multiple times, increase priority by one per appearance
                ordered_posts.add_task(post, ordered_posts.get_priority(post) + 1)
            else:
                ordered_posts.add_task(post)
    ans = -10
    while ans is None or ans < 0:
        #cycles only if user selects next page
        ans = generate_search_list(ordered_posts)
        if ans is not None and ans >= 0: #if it's a valid pid
            return ans
        elif ans is not None and ans == -2: #if no posts met search criteria
            return None
            
def generate_search_list(ordered_posts):
    """Shows user top five results that matched their search. Prompts user to select
    one of the posts, or move on to the next page (if there are more posts)

    Args:
        ordered_posts (Priority Queue): Contains all posts that met a search criteria, 
            ranked by number of times search critera was met

    Returns:
        [String/int]: Returns the pid of the post selected, or -1 to signify a next page,
            or -2 to signify that no posts met search criteria
    """     
    posts = []
    counter = count()

    #gets the first five (or less) results
    while next(counter) < 5:
        try:
            post = ordered_posts.pop_task()
            posts.append(post)
        except KeyError:
            break
    
    if len(posts) > 0:
        #if we found posts that matched the keyword(s)
        choice = cli.put_search_list(posts, ordered_posts.is_empty()) #gets user's chosen post or next page response
        if choice != 'Next Page':
            choice_list = choice.split(',')
            pid = int(choice_list[0][2:].split('\'')[0])
            return pid
        else: #user selected next page
            return -1
    else:
        #if no posts matched those keyword(s)
        return -2