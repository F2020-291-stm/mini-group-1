import cli
from database import Database, UserSession
import sys

def action_screen(session, database, pid):
    option = cli.action_menu_select(session.is_priviledged(), True)['action menu']
    if option == 'Post an answer':
        post_answer(pid, session, database)
    elif option == 'Vote on post':
        vote_post(pid, session, database)
    elif option == 'Mark as accepted answer':
        mark_accepted_answer(pid, database)
    elif option == 'Give a badge':
        give_badge(pid, database)
    elif option == 'Add a tag':
        pass
    elif option == 'Edit the post':
        pass

def post_answer(qid, session, database):
    answer = cli.post_answer()
    database.post_answers(session, answer['title'], answer ['body'], qid)

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

    

    