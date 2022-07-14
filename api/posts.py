from fastapi import APIRouter, Depends
from typing import List
from schemas import PostOut, PostIn, UserOut
from services.posts import PostService
from fastapi_pagination import Page, paginate
from services.auth import get_current_user

router = APIRouter(prefix='/posts')


@router.get('/', response_model=Page[PostOut])
def get_posts(source_id: int = None,
              user: UserOut = Depends(get_current_user),
              service: PostService = Depends()
              ):
    filters = {}
    if source_id:
        filters.update({'source_id': source_id, 'user_id': user.id})
    return paginate(service.get_all(filters=filters))


@router.post('/', response_model=PostOut)
def post_post(post_data: PostIn,
              service: PostService = Depends()
              ):
    return service.create(post_data)
