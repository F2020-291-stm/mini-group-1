import cli
import database_access
import sys

def master_menu_screen(user, database):
    choice = cli.master_menu_select()
    if choice['master menu'] == 'Post a question':
        post_question_screen(user, database)
    elif choice['master menu'] == 'Search for posts':
        pass
    elif choice['master menu'] == 'Logout':
        return False
    else:
        sys.exit(0)
        
def post_question_screen(user, database):
    print("\nEnter your question\n")
    question = cli.post_question()
    database.post_questions(user, question['title'], question['body'])
    
    

