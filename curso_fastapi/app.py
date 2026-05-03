from http import HTTPStatus

from fastapi import FastAPI

from curso_fastapi.routers import auth, users
from curso_fastapi.schemas import Message

app = FastAPI(
    title='Curso FastAPI',
    description='Curso administrado por Eduardo Mendes.',
    version='0.2',
)


app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Curso fastAPI'}
