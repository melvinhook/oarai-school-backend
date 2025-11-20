from datetime import datetime
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter,Depends, Form,HTTPException, UploadFile
from sqlalchemy.orm import Session 
from sqlalchemy import desc 
from ...models.Post import Posts,Comments,Replies,PostLikes,CommentLikes,ReplyLikes 
from ...models.Post.Posts import Posts as postmodel
from ...schemas.Post import scheme 
from ...dep import get_db   
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
router=APIRouter()  
cloudinary.config(
    cloud_name="dnu7wi9ck",
    api_key="614691958331998",
    api_secret="O4tCktZV_h_NhFymAnVaxqkyN5U"
)   
current_ids = set()  
def update_id_fit(db: Session, all_posts):
    global current_ids
    
    # ambil semua id dari hasil query
    new_ids = [p.id for p in all_posts]
    
    # cari id baru yang belum ada
    new_items_ids = set(new_ids) - current_ids
    
    if new_items_ids:
        print("🆕 ID baru ditemukan:", new_items_ids)
        # update current_ids
        current_ids.update(new_items_ids)
        # ambil data post yang id-nya termasuk baru
        new_items = [p for p in all_posts if p.id in new_items_ids]
        return new_items
    else:
        print("Tidak ada ID baru")
        return []  # biar selalu aman 
    





#   
#POST 
#     
@router.post("/posts/upload_cover")
async def upload_post_cover(
    post_id: int = Form(...),
    file: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    post = db.query(Posts.Posts).filter(Posts.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    public_id = f"post_covers/post_{post_id}_{timestamp}"
    upload_result = cloudinary.uploader.upload(
        file.file,
        folder="post_covers",
        public_id=public_id,
        overwrite=True,
        resource_type="image"
    )
    cover_url = upload_result.get("secure_url")
    if not cover_url:
        raise HTTPException(status_code=500, detail="Upload failed")
    post.cover = cover_url
    db.commit()
    return {"message": "Cover uploaded successfully", "cover_url": cover_url}
@router.post("/post",response_model=scheme.PostOut) 
def create_post(payload:scheme.PostCreate,db:Session=Depends(get_db)): 
    post_create=Posts.Posts( 
        title=payload.title,  
        slug=payload.slug,
        content=payload.content, 
        user_id=payload.user_id 
    )  
    db.add(post_create) 
    db.commit()  
    db.refresh(post_create) 
    return post_create 
@router.post("/comment",response_model=scheme.CommentOut) 
def create_post(payload:scheme.CommentCreate,db:Session=Depends(get_db)): 
    comment_create=Comments.Comments(
        content=payload.content,
        user_id=payload.user_id, 
        post_id=payload.post_id
    ) 
    db.add(comment_create) 
    db.commit() 
    db.refresh(comment_create) 
    return comment_create 
@router.post("/reply",response_model=scheme.ReplyOut) 
def create_reply(payload:scheme.ReplyCreate,db:Session=Depends(get_db)): 
    reply_create=Replies.Replies(
        content=payload.content, 
        user_id=payload.user_id, 
        comment_id=payload.comment_id
    ) 
    db.add(reply_create) 
    db.commit() 
    db.refresh(reply_create) 
    return reply_create   
@router.post("/postlikes",response_model=scheme.LikeResponse) 
def create_postlikes(payload:scheme.PostLikesCreate,db:Session=Depends(get_db)):  
    similar=db.query(PostLikes.PostLikes).filter(PostLikes.PostLikes.post_id==payload.post_id).first()   
    if similar:  
        db.delete(similar) 
        db.commit() 
        return {"liked": False, "message": "Unliked successfully"}
    else:
        postlikes_create=PostLikes.PostLikes(
            post_id=payload.post_id, 
            user_id=payload.user_id
        ) 
        db.add(postlikes_create) 
        db.commit() 
        db.refresh(postlikes_create) 
        return {"liked": True, "message": "Liked successfully"}  
@router.post("/commentlikes",response_model=scheme.LikeResponse) 
def create_commentlikes(payload:scheme.CommentLikesCreate,db:Session=Depends(get_db)): 
    similar=db.query(CommentLikes.CommentLikes).filter(CommentLikes.CommentLikes.comment_id==payload.comment_id).first() 
    if similar: 
        db.delete(similar) 
        db.commit() 
        return {"liked": False, "message": "Unliked successfully"} 
    else:
        commentlikes_create=CommentLikes.CommentLikes(
            comment_id=payload.comment_id, 
            user_id=payload.user_id
        ) 
        db.add(commentlikes_create) 
        db.commit() 
        db.refresh(commentlikes_create)  
        return {"liked": True, "message": "Liked successfully"}  
@router.post("/replylikes",response_model=scheme.LikeResponse) 
def create_commentlikes(payload:scheme.ReplyLikesCreate,db:Session=Depends(get_db)): 
    similar=db.query(ReplyLikes.ReplyLikes).filter(ReplyLikes.ReplyLikes.reply_id==payload.reply_id).first()  
    if similar: 
        db.delete(similar) 
        db.commit() 
        return {"liked": False, "message": "Unliked successfully"} 
    else:
        replylikes_create=ReplyLikes.ReplyLikes(
            reply_id=payload.reply_id, 
            user_id=payload.user_id
        ) 
        db.add(replylikes_create) 
        db.commit() 
        db.refresh(replylikes_create)  
        return {"liked": True, "message": "Liked successfully"} 
      
# 
#GET 
#  

@router.get("/post", response_model=list[scheme.PostOut]) 
def get_post(db: Session = Depends(get_db)): 
    return db.query(Posts.Posts).all() 
@router.get("/post/{post_id}",response_model=scheme.PostOut) 
def get_post_by_id(post_id:int,db:Session=Depends(get_db)): 
    return db.query(Posts.Posts).filter(Posts.Posts.id==post_id).first()  
@router.get("/comment/{post_id}",response_model=scheme.CommentResponse) 
def get_comment(post_id:int,db:Session=Depends(get_db)):    
    comments = db.query(Comments.Comments).filter(Comments.Comments.post_id==post_id).order_by(desc(Comments.Comments.created_at)).all()   
    new_posts = update_id_fit(db, comments) 
    return  {
        "comment": comments,
        "new_ids": new_posts  # kirim data post baru, bukan cuma id
    }  
@router.put("/post/{post_id}", response_model=scheme.PostOut)
def edit_post(payload: scheme.PostCreate, post_id: int, db: Session = Depends(get_db)):
    find_post = db.query(Posts.Posts).filter(Posts.Posts.id == post_id).first()
    if not find_post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} is not found")

    if payload.title is not None:
        find_post.title = payload.title
    if payload.content is not None:
        find_post.content = payload.content
    if payload.slug is not None:
        find_post.slug = payload.slug
    if payload.user_id is not None:
        find_post.user_id = payload.user_id

    db.commit()
    db.refresh(find_post)
    return find_post

    
""" 

    editing_post=Posts.Posts(
        title=payload.title,
        content=payload.content, 
        slug=payload.slug,  
        user_id=payload.user_id,  
        cover=payload.cover 
    )  

"""


""" 
@router.get("/posttest", response_model=posttest.PostResponse)
def get_posttest(db: Session = Depends(get_db)):
    posts = db.query(posttestmodel.PostTest)\
              .order_by(posttestmodel.PostTest.created_at.desc())\
              .all()
    new_posts = update_id_fit(db, posts)
    return {
        "posts": posts,
        "new_ids": new_posts  # kirim data post baru, bukan cuma id
    }
"""


@router.get("/reply/{comment_id}",response_model=scheme.ReplyOut) 
def get_reply(comment_id:int,db:Session=Depends(get_db)): 
    get_replies=db.query(Replies.Replies).filter(Replies.Replies.comment_id==comment_id).first() 
    if not get_replies: 
        raise HTTPException(status_code=401,detail="Not Found") 
    return get_replies 
    
# 
#TEST 
# 
 
@router.get("/comment",response_model=list[scheme.CommentOut]) 
def get_comment(db:Session=Depends(get_db)): 
    return db.query(Comments.Comments).all()  


