from os import stat
from fastapi import FastAPI
from fastapi import HTTPException, status
from pydantic import BaseModel
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from starlette.responses import Response

from sqlalchemy.orm import Session
from fastapi import Depends

from . import models
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='api', user="postgres",
                                password="GAILLOTY236", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database has failed")
        print("Error", error)
        time.sleep(2)


@app.get("/")
def index():
    return {"message": "Hello, welcome !"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    id_str = str(id)
    cursor.execute("SELECT * FROM posts WHERE id = %s ;", (id_str,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id_str} not found.")
    return {"data": post}


@app.post("/posts/{id}")
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published)
    VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    str_id = str(id)
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING *", (str_id,))
    deleted_post = cursor.fetchone()
    conn.commit
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id {str_id} is not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    str_id = str(id)
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str_id,))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {str_id} does not exist.")
    return {"data": updated_post}


@app.get("/sqlalchemy")
def home_sqlalchemy(db: Session = Depends(get_db)):
    return {"status": "success"}
