from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # A integração do ORM não funciona com o esquema do pydantic,
    # sendo necessário incluir o 'modela_config' para que haja
    # a conversão direta do objeto do SQLAlchemy com eschemas
    # pydantic
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserUnique(BaseModel):
    user: UserPublic


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    # 'ge' -> significa greater than [maior que]
    skip: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=100)
