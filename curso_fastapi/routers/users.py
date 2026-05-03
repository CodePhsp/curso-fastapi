from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
    UserUnique,
)
from curso_fastapi.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['Users'])
SessionType = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# session: Session = Depends(get_session) diz que a função get_session
# será executada antes da execução da função
# e o valor retornado por get_session
# será atribuído ao parâmetro session.
def create_user(user: UserSchema, session: SessionType):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: SessionType,
    filter_users: Annotated[FilterPage, Query()],
):
    users = session.scalars(
        select(User).offset(filter_users.skip).limit(filter_users.limit)
    ).all()
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: SessionType,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    # status code: 409
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists.',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: SessionType, current_user: CurrentUser):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/{user_id}', response_model=UserUnique)
def search_unique_user(user_id: int, session: SessionType):

    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return {'user': user}
