from sqlalchemy import create_engine
 
engine = create_engine('sqlite:///file_name?check_same_thread=False')