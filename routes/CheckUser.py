from fastapi import Depends, HTTPException
from requests import Session

from backend.dep import get_db
from backend.models.Users import models
from backend.routes.user.auth import get_current_user


def get_user_verify(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = db.query(models.User.first_name, models.User.last_name, models.User.profile_photos).filter(models.User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found") 
    return {"firstname": user.first_name, "lastname": user.last_name, "profile_photo": user.profile_photos}