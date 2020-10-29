import cli
import database_access
import sys
from util import PQ
from itertools import count
from action_screen import action_screen
#from copy import deepcopy

def master_menu_screen(user, database):
    choice = cli.master_menu_select()
    if choice['master menu'] == 'Post a question':
        post_question_screen(user, database)
        return True
    elif choice['master menu'] == 'Search for posts':
        pid = search_questions(user, database)
        if pid is not None:
            pid = str(pid)
            logged = action_screen(user, database, pid)
        else:
            print('No matches')
            logged = True
        return logged
    elif choice['master menu'] == 'Logout':
        return False
    else:
        sys.exit(0)
        
def post_question_screen(user, database):
    print("\nEnter your question\n")
    question = cli.post_question()
    database.post_questions(user, question['title'], question['body'])
    
def search_questions(user, database):
    print("\nSearching the database....\n")
    print("Enter Search Keywords seperated by \';\'\n")
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
        if ans is not None and ans > 0:
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
        choice = cli.put_search_list(posts, ordered_posts.is_empty())['search menu']
        if choice != 'Next Page':
            choice_list = choice.split(',')
            pid = int(choice_list[0][2:].split('\'')[0])
            return pid
        else:
            return -1
    else:
        return -2
    
    
