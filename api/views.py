from fastapi import APIRouter, Depends, Request
from schemas import PostOut
from services.posts import PostService
from fastapi.templating import Jinja2Templates
from fastapi_pagination import paginate
from api.helpers import Page


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/', response_model=Page[PostOut])
def get_posts(request: Request,
              source_id: int = None,
              service: PostService = Depends()
              ):
    filters = {}
    if source_id:
        filters.update({'source_id': source_id})
    paginator = paginate(service.get_all(filters=filters))
    return templates.TemplateResponse("posts.html",
                                      {"request": request,
                                       "posts": paginator.items,
                                       "page": paginator.page
                                       }
                                      )
