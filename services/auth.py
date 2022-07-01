from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from models.database import get_session
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.models_orm import User
from schemas import UserOut, UserIn, Token
from passlib.hash import bcrypt
from settings import settings
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(
                                    tokenUrl='/auth/sign-in'  # url где доступна авторизация для ридеректа
                                     )


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """ чтение токена из хэдера"""
    return AuthService.validate_token(token)


class AuthService:
    """ Авторизация """
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """ проверка хэшированного пароля """
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """ хэширование пароля """
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> UserOut:
        """ валидация пользователя """
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(token,
                                 settings.jwt_secret,
                                 algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise exception from None

        user_data = payload.get('user')
        try:
            user = UserOut.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: UserOut) -> Token:
        """ создание токена """
        user_data = UserOut.from_orm(user)  # из orm в pydantic

        user_data.created_at = datetime.strftime(user_data.created_at, "%Y-%m-%d %H:%M:%S", )
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_user_by_username_or_email(self, username, email):
        user = (
            self.session.query(User)
            .filter(or_(User.username == username, User.email == email))
            .first()
        )
        return user

    def register_new_user(self, user_data: UserIn) -> Token:
        """ создание - авторизация пользователя """
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='username or email is exists already',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        if self._get_user_by_username_or_email(username=user_data.username, email=user_data.email):
            raise exception
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        user = (
            self.session.query(User)
            .filter(User.username == username)
            # .filter()
            .first()
        )
        if not user:
            raise exception
        if not self.verify_password(password, user.password_hash):  # если не пароль не проходит
            raise exception
        return self.create_token(user)
