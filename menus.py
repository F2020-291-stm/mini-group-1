import cli
import sys

from util import PQ
from itertools import count

# SUBMENU
def handle_submenu(session, database, pid):
    option = cli.action_menu_select(session.is_privileged(), database.is_answer(pid))
    if option == 'Post an answer':
        post_answer(pid, session, database)
    elif option == 'Vote on post':
        vote_post(pid, session, database)
    elif option == 'Mark as accepted answer':
        mark_accepted_answer(pid, database)
    elif option == 'Give a badge':
        give_badge(pid, database)
    elif option == 'Add a tag':
        add_tag(pid, database)
    elif option == 'Edit the post':
        edit_post(pid, database)

def post_answer(qid, session, database):
    answer = cli.write_post()
    database.post_answer(session, answer['title'], answer ['body'], qid)

def vote_post(pid, session, database):
    voted = database.vote_post(session, pid)
    if voted:
        print('Cannot Vote : Already Voted on Post')
    else:
        print('Vote Recorded')

def mark_accepted_answer(pid, database):
    if not database.mark_accepted_answer(pid):
        if cli.force_mark_answer():
            database.mark_accepted_answer(pid, force=True)

def give_badge(pid, database):
    badge_names = database.get_badge_list()
    chosen_name = cli.choose_badge(badge_names)
    database.give_badge(pid, chosen_name)

def add_tag(pid, database):
    database.add_tag(pid, cli.request_tag())

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
    choice = cli.master_menu_select()
    if choice == 'Post a question':
        post_question_screen(session, database)
    elif choice == 'Search for posts':
        pid = search_questions(database)
        if pid is not None:
            pid = str(pid)
            handle_submenu(session, database, pid)
        else:
            print('No matches')
    elif choice == 'Logout':
        session.logout()
    else:
        sys.exit(0)

def post_question_screen(session, database):
    print("\nEnter your question\n")
    question = cli.write_post()
    database.post_questions(session, question['title'], question['body'])
    
def search_questions(database):
    print("\nSearching the database....\n")
    keywords = cli.get_keyword()['keywords']
    keywords_list  = [string.strip() for string in keywords.split(';')]
    ordered_posts = PQ() # convert dict to PQ
    for keyword in keywords_list:
        posts = database.search_posts(keyword)
        for post in posts:
            if ordered_posts.check_if_in_queue(post):
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
    while next(counter) < 5:
        try:
            post = ordered_posts.pop_task()
            posts.append(post)
        except KeyError:
            break
    if len(posts) > 0:
        choice = cli.put_search_list(posts, ordered_posts.is_empty())
        if choice != 'Next Page':
            choice_list = choice.split(',')
            pid = int(choice_list[0][2:].split('\'')[0])
            return pid
        else:
            return -1
    else:
        return -2