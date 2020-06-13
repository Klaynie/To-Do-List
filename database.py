from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())
 
    def __repr__(self):
        return self.task

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

if __name__ == "__main__":
    Base.metadata.create_all(engine)