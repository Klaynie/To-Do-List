from enum import IntEnum

class MenuItem(IntEnum):
    EXIT = 0
    TODAY = 1
    ADD_TASK = 2

keep_going = True

def exit():
    global keep_going
    keep_going = False
    print('\n')
    print('Bye')
    return None

def get_task_list():
    print("Nothing to do!")
    return None

def set_task():
    print("Enter task")
    user_input = input()
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

def input_handler():
    action = get_menu_entry()
    if action == MenuItem.TODAY:
        get_task_list()
    elif action == MenuItem.ADD_TASK:
        set_task()
    elif action == MenuItem.EXIT:
        exit()

def menu_loop():
    global keep_going
    while keep_going:
        print(get_menu_text())
        input_handler()

if __name__ == "__main__":
    menu_loop()