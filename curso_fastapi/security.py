from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.settings import Settings

pwd_context = PasswordHash.recommended()

settings = Settings()  # pyright: ignore[reportCallIssue]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


# token:
# garante que um token foi enviado, caso não tenha sido
# enviado ele redirecionará a tokenUrl do objeto OAuth2PasswordBearer.
def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')

        # verifica se o email está no payload
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        # verifica se o token é um token JWT válido
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        # verifica se o email enviado está na base de dados
        raise credentials_exception

    return user
