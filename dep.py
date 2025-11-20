from .database import local 
def get_db(): 
    db=local() 
    try: 
        yield db  
    finally: 
        db.close()