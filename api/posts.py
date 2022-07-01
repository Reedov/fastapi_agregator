from fastapi import APIRouter, Depends
from typing import List
from schemas import PostOut, PostIn
from services.posts import PostService
from fastapi_pagination import Page, paginate

router = APIRouter(prefix='/posts')


@router.get('/', response_model=Page[PostOut])
def get_posts(source_id: int = None,
              service: PostService = Depends()
              ):
    filters = {}
    if source_id:
        filters.update({'source_id': source_id})
    return paginate(service.get_all(filters=filters))


@router.post('/', response_model=PostOut)
def post_post(post_data: PostIn,
              service: PostService = Depends()
              ):
    return service.create(post_data)
