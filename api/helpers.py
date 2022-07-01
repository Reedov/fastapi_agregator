from fastapi import Query
from fastapi_pagination import Params as BaseParams, Page as BasePage
from typing import TypeVar, Generic, Sequence


T = TypeVar("T")


class Params(BaseParams):
    """ переопределение параметров пагинатора """
    size: int = Query(10, ge=1, le=1_000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
