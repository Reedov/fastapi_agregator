from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)


# class SubscribeBase(BaseModel):
#     source_id: int = Field(None)
#
#
# class SubscribeIn(SubscribeBase):
#     # user_id: int = Field(None)
#     ...
#
#
# class SubscribeOut(SubscribeBase):
#     id: int = Field(...)

class SourceTypeBase(BaseModel):
    name: str = Field(None, description='название типа ресурса')


class SourceTypeIn(SourceTypeBase):
    ...


class SourceTypeOut(SourceTypeBase):
    id: int = Field(..., description='id типа ресурса')

    class Config:
        orm_mode = True


class SourceBase(BaseModel):
    name: str = Field(None, description="Имя ресурса")
    url: str = Field(None, description='url ресурса')
    get_items: int = Field(None, description='кол-во')
    is_active: bool = Field(None, description='активно')
    get_period_sec: int = Field(None, description='период получения, секунд')
    created_at: datetime = Field(None, description='время создания')


class SourceIn(SourceBase):
    """ схема Source на вход """
    type_id: int = Field(None, description='ид типа источника')


class SourcePatchOut(SourceBase):
    id: int = Field(None, description='id ресурса')
    type_id: int = Field(None, description='ид типа источника')

    class Config:
        orm_mode = True


class SourceOut(SourceBase):
    """ схема Source на выход """
    id: int = Field(None, description='id ресурса')
    type: str = Field(None, description='тип ресурса')

    class Config:
        orm_mode = True


class SourseFilters(BaseModel):
    get_items: int = Field(None, description='кол-во')
    is_active: bool = Field(None, description='активно')


class SourceGetIn(BaseModel):
    source_id: int = Field(..., description='id ресурса')
    get_at: datetime = Field(..., description='время посещения')


class PostIn(BaseModel):
    """ схема Post на вход """
    posted_at: datetime = Field(..., description='Дата-Время поста')
    title: str = Field(..., description='Название')
    content: str = Field(None, description='Содержимое поста')
    url: str = Field(None, description='Ссылка на пост')
    img_url: str = Field(None, description='Ссылка на картинку поста')
    source_id: int = Field(None, description='ИД источника')


class PostOut(PostIn):
    """ схема Post на выход """
    id: int = Field(..., description='id поста')

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    # sources: List[SourceBase] = []


class UserIn(UserBase):
    password: str = Field(...)
    second_name: str = Field(None)
    first_name: str = Field(None)


class UserOut(UserBase):
    id: int = Field(...)
    # subscribes: List[SourceIn] = Field(None)
    created_at: datetime = Field(None, description='дата создания')
    # updated_at: datetime.datetime = Field(...)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Subscribe(BaseModel):
    user_id: int
    source_id: int


class SubscribesOut(BaseModel):
    user_id: int
    sources: List[SourceOut]
