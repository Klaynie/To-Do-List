import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import datetime, timedelta
from enum import IntEnum


Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class MenuItem(IntEnum):
    EXIT = 0
    TODAY = 1
    WEEK = 2
    ALL_TASKS = 3
    MISSED_TASKS = 4
    ADD_TASK = 5
    DELETE_TASK = 6

class TaskListOptions(IntEnum):
    TASK = 1
    DEADLINE = 2

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
keep_going = True


def exit():
    global keep_going
    keep_going = False
    print('\nBye!')


def convert_string_to_datetime(string):
    return datetime.strptime(string, '%Y-%m-%d') # YYYY-MM-DD


def set_task(session):
    print("Enter task")
    user_input_task = input()
    print("Enter deadline")
    user_input_deadline = input()
    user_input_deadline = convert_string_to_datetime(user_input_deadline)
    new_row = Table(task=user_input_task, deadline=user_input_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added")


def get_database_rows(session, date):
    return session.query(Table).filter(Table.deadline == date).all()

def get_result_set(query):
    connection = engine.connect()
    metadata = db.MetaData()
    result_proxy = connection.execute(query)
    result = result_proxy.fetchall()
    return result

def get_missed_tasks(session, date):
    table = get_database_table(session)
    query = db.select([table]).where(table.c.deadline < date).order_by(table.c.deadline, table.c.id)
    result_set = get_result_set(query)
    return result_set

def get_missed_task_list(session, date):
    table = get_missed_tasks(session, date)
    print('\n')
    print("Missed tasks:")
    if len(table) == 0:
        print("Nothing is missed!")
    else:
        print_task_list(table)
    print('\n')


def delet_row(session, id_to_delete):
    session.query(Table).filter(Table.id == id_to_delete).delete()
    session.commit()


def generate_user_number_2_id_dict(task_list):
    result = {}
    for counter, item in enumerate(task_list, 1):
        task_id = item[0]
        result[counter] = task_id
    return result

def delete_task(session, task_list, user_number):
    user_number_2_id_dict = generate_user_number_2_id_dict(task_list)
    id_to_delete = user_number_2_id_dict[user_number]
    delet_row(session, id_to_delete)
    print("The task has been deleted!")
    print("\n")


def print_task_list(table):
    for counter, item in enumerate(table, 1):
            task = item[int(TaskListOptions.TASK)]
            deadline = item[int(TaskListOptions.DEADLINE)]
            print(str(counter) + '.', task + '.', datetime.strftime(deadline, '%d %b'))


def print_tasks_to_delete_list(table):
    print('\n')
    if len(table) == 0:
        print("Nothing to delete")
    else:
        print("Chose the number of the task you want to delete:")
        print_task_list(table)
    print('\n')


def task_deletion(session, date):
    task_list = get_missed_tasks(session, date)
    print_tasks_to_delete_list(task_list)
    if len(task_list) != 0:
        task_to_delete_number = int(input())
        delete_task(session, task_list, task_to_delete_number)


def get_date():
    return datetime.now().date()


def get_database_table(session):
    global engine
    connection = engine.connect()
    metadata = db.MetaData()
    return db.Table('task', metadata, autoload=True, autoload_with=engine)


def get_all_tasks(session):
    table = get_database_table(session)
    query = db.select([table]).order_by(table.c.deadline, table.c.id)
    result_set = get_result_set(query)
    return result_set


def get_all_task_list(session):
    result_set = get_all_tasks(session)
    print('\n')
    print("All tasks:")
    print_task_list(result_set)
    print('\n')


def get_week_task_list(session, date):
    for delta_days in range(8):
        rows = get_database_rows(session, date)
        generate_task_message(rows, date)
        date = date + timedelta(days=1)


def get_today_task_list(session, date):
    rows = get_database_rows(session, date)
    generate_task_message(rows, date, today=True)


def generate_task_message(rows, date, today=False):
    print('\n')
    message = "Nothing to do!"
    date_string_today = f"Today {datetime.strftime(date, '%d %b')}"
    other_date_string = f"{datetime.strftime(date, '%A %d %b')}"
    if len(rows) == 0:
        if today:
            print(message)
        else:
            print(other_date_string)
            print(message)
    else:
        print(date_string_today if today else other_date_string)
        for counter, task in enumerate(rows, 1):
            print(str(counter) + '.', task)


def get_menu_entry():
    return int(input())


def get_menu_text():
    result = "1) Today's tasks\n" \
             "2) Week's tasks\n" \
             "3) All tasks\n" \
             "4) Missed tasks\n" \
             "5) Add task\n" \
             "6) Delete task\n" \
             "0) Exit"
    return result


def input_handler(session, date):
    action = get_menu_entry()
    if action == MenuItem.TODAY:
        get_today_task_list(session, date)
    elif action == MenuItem.WEEK:
        get_week_task_list(session, date)
    elif action == MenuItem.ALL_TASKS:
        get_all_task_list(session)
    elif action == MenuItem.MISSED_TASKS:
        get_missed_task_list(session, date)
    elif action == MenuItem.ADD_TASK:
        set_task(session)
    elif action == MenuItem.DELETE_TASK:
        task_deletion(session, date)
    elif action == MenuItem.EXIT:
        exit()


def menu_loop(session):
    global keep_going
    while keep_going:
        date = get_date()
        print(get_menu_text())
        input_handler(session, date)


menu_loop(session)