from sqlalchemy.orm import sessionmaker
from database import *

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    new_row = Table(task='Test',
             deadline=datetime.now)
    session.add(new_row)
    session.commit()

    rows = session.query(Table).all()

    first_row = rows[0] # In case rows list is not empty

    print(first_row.string_field) # Will print value of the string_field
    print(first_row.id) # Will print the id of the row.
    print(first_row) # Will print the string that was returned by __repr__ method