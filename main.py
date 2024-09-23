from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()


@app.get('/')
def index():
    return {'data': {
        'name': 'Ramna',
        'age': 24
    }}


@app.get('/about')
def about():
    return {'data': {
        'page': 'This is About Page'
    }}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


# @app.post('/blog')
# def create_post(request: Blog):
#     return {'data': f'{request.title} {request.body}'}

@app.post('/blog')
def create_post(blog: Blog):
    return {'data': f'{blog.title} {blog.body}'}


@app.get('/blog')
def blog(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    return {'data': f'limit : {limit} and published : {published}'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port='9000')
    # run command python main.py
