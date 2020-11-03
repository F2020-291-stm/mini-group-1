import cli
import sys

from util import PQ
from itertools import count

# SUBMENU
def handle_submenu(session, database, pid):
    #once a user has searched for a post, they can do a multitude
    #of things with that post

    #user determines an option. options available are determined within cli.action_menu_select
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
    #writes an answer and informs database that this new post answers qid
    answer = cli.write_post()
    database.post_answer(session, answer['title'], answer ['body'], qid)

def vote_post(pid, session, database):
    #upvotes the post
    success = database.vote_post(session, pid)
    if not success: #user has already upvoted this post
        print('Cannot Vote : Already Voted on Post')
    else: #otherwise, vote goes through
        print('Vote Recorded')

def mark_accepted_answer(pid, database):
    #sets pid to be the answer to the question, but if the question already
    #has a "the answer", then ask user if they want to switch the question's 
    #"the answer" over to this new answer anyways
    if not database.mark_accepted_answer(pid): 
        if cli.force_mark_answer():
            database.mark_accepted_answer(pid, force=True)

def give_badge(pid, database):
    #gets all badge names from database,
    #gets user to pick one of them,
    #then gives that badge to the user who wrote the post
    badge_names = database.get_badge_list()
    chosen_name = cli.choose_badge(badge_names)
    database.give_badge(pid, chosen_name)

def add_tag(pid, database):
    #asks user for tags and tags the post with each one
    for tag in cli.request_tag():
        database.add_tag(pid, tag)

def edit_post(pid, database):
    post = database.get_post(pid)
    post = cli.edit_post(post[0], post[1])
    database.update_post(pid, post['title'], post['body'])

# LOGIN MENU
def handle_login(database):
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
    #queries user to choose between posting a question, searching, logging out, or quitting
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
    print("\nEnter your question\n")
    #User enters title and body for question and it gets uplaoded to database
    question = cli.write_post()
    database.post_questions(session, question['title'], question['body'])
    
def search_questions(database):
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
        ans = generate_search_list(ordered_posts)
        if ans is not None and ans >= 0:
            return ans
        elif ans is not None and ans == -2:
            return None
            
def generate_search_list(ordered_posts):  
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
        else:
            return -1
    else:
        #if no posts matched those keyword(s)
        return -2