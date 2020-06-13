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
    ADD_TASK = 4


class TaskColumn(IntEnum):
    ID = 0
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
    print('\n')
    print('Bye!')
    return None


def set_task(session):
    print("Enter task")
    user_input_task = input()
    print("Enter deadline")
    user_input_deadline = input()
    user_input_deadline = datetime.strptime(user_input_deadline, '%Y-%m-%d')
    new_row = Table(task=user_input_task, deadline=user_input_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added")
    return None


def get_database_rows(session, date):
    return session.query(Table).filter(Table.deadline == date).all()


def get_date():
    return datetime.now().date()


def get_database_table(session):
    global engine
    connection = engine.connect()
    metadata = db.MetaData()
    return db.Table('task', metadata, autoload=True, autoload_with=engine)


def get_all_task_list(session):
    table = get_database_table(session)
    connection = engine.connect()
    metadata = db.MetaData()
    query = db.select([table]).order_by(table.c.deadline, table.c.id)
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    print('\n')
    print("All tasks: ")
    for counter, item in enumerate(result_set, 1):
        task = item[1]
        deadline = item[2]
        print(str(counter) + '.', task + '.', datetime.strftime(deadline, '%d %b'))
    print('\n')


def get_week_task_list(session, date):
    for delta_days in range(7):
        date = date + timedelta(days=delta_days)
        rows = get_database_rows(session, date)
        generate_task_message(rows, date)


def get_today_task_list(session, date):
    rows = get_database_rows(session, date)
    generate_task_message(rows, date, today=True)
    return None


def generate_task_message(rows, date, today=False):
    print('\n')
    if len(rows) == 0:
        if today:
            print("Nothing to do!")
        else:
            print(f"{datetime.strftime(date, '%A %d %b')}")
            print("Nothing to do!")
    else:
        print(f"Today {datetime.strftime(date, '%d %b')}:" if today else f"{datetime.strftime(date, '%A %d %b')}")
        for counter, task in enumerate(rows, 1):
            print(str(counter) + '.', task)
    print('\n')


def get_menu_entry():
    result = ''
    try:
        result = int(input())
    except Exception:
        print("Please enter the item number!")
    return result


def get_menu_text():
    result = "1) Today's tasks\n" \
             "2) Week's tasks\n" \
             "3) All tasks\n" \
             "4) Add task\n" \
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
    elif action == MenuItem.ADD_TASK:
        set_task(session)
    elif action == MenuItem.EXIT:
        exit()


def menu_loop(session):
    global keep_going
    while keep_going:
        date = get_date()
        print(get_menu_text())
        input_handler(session, date)


menu_loop(session)