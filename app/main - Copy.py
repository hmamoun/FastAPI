import random
from typing import Optional
from fastapi import FastAPI , Response, exceptions , status , HTTPException , Depends
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
from sqlalchemy import engine
from  sqlalchemy.orm import session
from sqlalchemy.util.langhelpers import public_factory

from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
import psycopg2
from  psycopg2.extras import RealDictCursor

import time
from . import models
from .database import engine ,  get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()



class Post(BaseModel):
    id:Optional[int ]
    title: str
    content: str
    published: bool = True
    


while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi' ,user = 'fastapiuser',password='password1231' , cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successsful')
        break
    except Exception as error:
        print("Connecting to database failed")
        print("The error: " , error)
        time.sleep(2)




my_posts = [{"title":"title of post 1" , "content":"content of post1" , "id":1},
        {"title":"favorite food" , "content":"Pizza1" , "id":2}]



def find_post(id):
    for  x in my_posts:
        if int(x['id'])==int(id):

            return {"data": x}

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id: 
            return i


#path operation / rout


@app.get("/sqlalchemy")
def test_posts(db:session = Depends(get_db)):
    post = db.query(models.Post).all()
    return{"Data":post}

@app.get("/")
async def root():
    #return '<h1>hayan</h1>'
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts(db:session = Depends(get_db)):
    post = db.query(models.Post).all()    
    # cursor.execute(""" SELECT * FROM POSTS""")
    # post = cursor.fetchall()
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id:int,db:session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail =f"post with id {id} not found" )
    return {"data": post}  
    # cursor.execute(""" SELECT * FROM posts where id = %s""" , (str(id),) )
    # post = cursor.fetchone()
    # post = db.query(models.Post).all()       
       

@app.post("/posts")
def create_posts(post: Post , db:session = Depends(get_db)):
    #new_post = models.Post(title=post.title ,content = post.content , published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(""" INSERT INTO POSTS(title , content, published) VALUES (%s,%s,%s) RETURNING * """ , (post.title , post.content , post.published) )
    # new_post = cursor.fetchone()
    # conn.commit()
    return{"message":new_post}


@app.get("/latestposts")
def get_posts():
    return {"data": my_posts[len(my_posts)-1]}


@app.delete("/posts/{id}" , status_code=  status.HTTP_204_NO_CONTENT)
def deletepost(id:int, db:session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id)
    
    if post.first() ==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist") 
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""" ,(str(id),) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    #index = find_index_post(id)
    # if deleted_post ==None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist") 
    #my_posts.pop(index)
    #return Response(status_code = status.HTTP_204_NO_CONTENT)
    #return {'message': 'post was successfully deleted'}


@app.put("/posts/{id}")
def update_post(id: int, updated_post:Post, db:session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()
    #print (newpost)
    if post ==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist") 
    post_query.update(updated_post.dict(),synchronize_session = False)
    
#    post_query.update({"title":"tSarasarasaraed title" , "content": "updatecontent"},synchronize_session = False)
    db.commit()
    return {"data": "updated"}

    # cursor.execute(""" UPDATE posts set title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ ,(post.title , post.content , post.published , str(id),) )
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # #index = find_index_post(id)
    # if updated_post ==None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist") 
    # # post_dict =  post.dict()
    # # post_dict['id'] = id
    # # my_posts[index] =post_dict
    
    #return {"data": updated_post}
