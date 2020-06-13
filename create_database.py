from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()

class Table(Base):
    __tablename__ = 'table_name'
    id = Column(Integer, primary_key=True)
    string_field = Column(String, default='default_value')
    date_field = Column(Date, default=datetime.today())
 
    def __repr__(self):
        return self.string_field

engine = create_engine('sqlite:///file_name?check_same_thread=False')
Base.metadata.create_all(engine)