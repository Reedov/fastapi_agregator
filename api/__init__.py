from fastapi import APIRouter

from .sources import router as sources_router
from .posts import router as posts_router
from .auth import router as auth_router
from .user import router as user_router
from .views import router as views_router

router = APIRouter()

router.include_router(sources_router)
router.include_router(posts_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(views_router)