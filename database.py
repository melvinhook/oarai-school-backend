from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base 
database_url="postgresql://postgres:XaWeYSEbBPyLzrMUwTMFJyjdfpeEmHDj@shuttle.proxy.rlwy.net:20765/railway" 
engine=create_engine(database_url) 
local=sessionmaker(autocommit=False,autoflush=False,bind=engine) 
base=declarative_base() 
