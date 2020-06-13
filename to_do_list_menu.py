from enum import IntEnum
from database_session import *

class MenuItem(IntEnum):
    EXIT = 0
    TODAY = 1
    ADD_TASK = 2

keep_going = True

def exit():
    global keep_going
    keep_going = False
    print('\n')
    print('Bye!')
    return None

def get_task_list(session):
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        print("Today:")
        for counter, task in enumerate(rows, 1):
            print(str(counter) + '.', task)
    return None

def set_task(session):
    print("Enter task")
    user_input = input()
    new_row = Table(task=user_input)
    session.add(new_row)
    session.commit()
    print("The task has been added")
    return None

def get_menu_entry():
    result = ''
    try:
        result = int(input())
    except Exception:
        print("Please enter the item number!")
    return result

def get_menu_text():
    result = "1) Today's tasks\n" \
             "2) Add task\n" \
             "0) Exit"
    return result

def input_handler(session):
    action = get_menu_entry()
    if action == MenuItem.TODAY:
        get_task_list(session)
    elif action == MenuItem.ADD_TASK:
        set_task(session)
    elif action == MenuItem.EXIT:
        exit()

def menu_loop(session):
    global keep_going
    while keep_going:
        print(get_menu_text())
        input_handler(session)

if __name__ == "__main__":
    menu_loop(session)