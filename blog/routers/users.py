from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
import models
import database
import schemas
from repository import hashing

router = APIRouter(
    # tags=['Users']
    # xprefix='/users'
)


@router.post('/register', tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(email=request.email,
                           hashed_password=hashing.get_password_hash(request.hashed_password), is_active=request.is_active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{email}', response_model=schemas.UserResponceModel, tags=['Users'])
def get_user(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user.hashed_password = '**********'
    return user
