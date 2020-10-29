import cli
from database_access import Database
import sys

def action_screen(user, database, pid):
    option = cli.action_menu_select()['action menu']
    if option == 'Post an answer':
        post_answer(pid, user, database)
        return True
    elif option == 'Vote on post':
        vote_post(pid, user, database)
        return True
    elif option == 'Accept the answer':
        return True
    elif option == 'Give a badge':
        return True
    elif option == 'Add a tag':
        return True
    elif option == 'Edit the post':
        return True
    elif option == 'Logout':
        return False
    else:
        sys.exit(0)
    

def post_answer (qid, user, database):
    answer = cli.post_answer()
    database.post_answers(user, answer['title'], answer ['body'], qid)

def vote_post (pid, user, database):
    voted = database.vote_post(user, pid)
    if voted:    
        print('Cannot Vote : Already Voted on Post')
    else:
        print('Vote Recorded')
    