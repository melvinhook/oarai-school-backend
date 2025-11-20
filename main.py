from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from . import database   
from .models.Post.Replies import base as replybase 
from .models.Post.PostLikes import base as postbase 
from .models.Post.CommentLikes import base as commentlikes 
from .models.Post.ReplyLikes import base as replylikes 
from .models.Test.posttest import base as posttest
from .routes.user.routes import router  
from .routes.test.test import router as testrouter    
from .routes.post.post import router as postrouter  

database.base.metadata.create_all(bind=database.engine) 
replybase.metadata.create_all(bind=database.engine) 
postbase.metadata.create_all(bind=database.engine)  
commentlikes.metadata.create_all(bind=database.engine) 
replylikes.metadata.create_all(bind=database.engine) 
posttest.metadata.create_all(bind=database.engine)   


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)
app.include_router(router) 
app.include_router(testrouter) 
app.include_router(postrouter)
