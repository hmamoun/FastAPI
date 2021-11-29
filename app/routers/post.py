from fastapi import FastAPI , Response, exceptions , status , HTTPException , Depends , APIRouter
from typing import Optional , List
from sqlalchemy import func
#from fastapi.security import oauth2


from .. import models, schemas , oauth2
from sqlalchemy.orm import session
from ..database import   get_db

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

#Get all posts
#@router.get("/", response_model =List[schemas.Post] )
@router.get("/" , response_model =List[schemas.PostOut] )
def get_posts(db:session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user),limit: int=5 , skip:int=0 , search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).filter(models.Post.title.contains(search) ).limit(limit).offset(skip).all()
    results = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.owner_id==current_user.id).filter(
                models.Post.title.contains(search) ).limit(limit).offset(skip).all()
    return  results

#Get a specific post
@router.get("/{id}", response_model = schemas.PostOut )
def get_post(id:int,db:session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post)

    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail =f"post with id {id} not found" )
    return  post

#create a new post
@router.post("/" , status_code=status.HTTP_201_CREATED , response_model = schemas.Post )
def create_posts(post: schemas.PostCreate , db:session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
#    print(current_user.email)

    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#delete post
@router.delete("/{id}" , status_code=  status.HTTP_204_NO_CONTENT)
def deletepost(id:int, db:session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post ==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist") 
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can only delete your own posts") 
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

#update post
@router.put("/{id}", response_model = schemas.Post )
def update_post(id: int, update_post:schemas.PostCreate, db:session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post ==None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
  
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You can only delete your own posts") 
                                
    newpost = update_post.dict()
    newpost['id'] = id
    post_query.update(newpost,synchronize_session = False)                            
    db.commit()
    return post_query.first()
