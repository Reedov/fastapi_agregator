from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    db_user: str = 'user'
    db_password: str = 'password'
    db_host: str = 'sqlite:///database.db'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 120


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)

"""
from secrets import token_urlsafe
token_urlsafe(32)
"""

