from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import database
import schemas
from repository import JWTtoken

router = APIRouter(
    # tags=['Users']
    # xprefix='/users'
)


# @app.get('/blog')
# def showBlogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@router.get('/blog', response_model=List[schemas.BlogResponceModel], tags=['Blogs'])
def all_blogs(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(JWTtoken.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title,
                           body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# using Responce Model
@router.get('/blog/{id}', response_model=schemas.BlogResponceModel, tags=['Blogs'])
def get_blog(id: int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" blog id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f"Blog with the id {id} is not available"}

    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def delete_blog(id: int, response: Response, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(JWTtoken.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return blog


@router.put('/blog', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).update(
    #     {models.Blog.title: request.title, models.Blog.body: request.body}, synchronize_session=False)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first():
        # blog.update(request) #check why it gives error
        blog.update({models.Blog.title: request.title,
                    models.Blog.body: request.body})
        db.commit()
        return blog.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
