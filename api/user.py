from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserOut, SubscribesOut
from services.user import UserService
from .auth import get_current_user

router = APIRouter(prefix='/user')


@router.get('/', response_model=UserOut)
def get_source_by_id(
                     user: UserOut = Depends(get_current_user),
                     service: UserService = Depends()
                     ):
    """ получение пользователя по id (аналогично /auth/me )"""
    return service.get_by_id(user_id=user.id)


@router.get('/subscribes/', response_model=SubscribesOut)
def get_user_subscribes(
                        user: UserOut = Depends(get_current_user),
                        service: UserService = Depends(),
                        ):
    """ получение подписок пользователя """
    return service.get_user_subscribes(user_id=user.id)


@router.patch('/subcribes/', response_model=SubscribesOut)
def update_user_subscribes(
                           subscribes: List[int],
                           user: UserOut = Depends(get_current_user),
                           service: UserService = Depends()):
    """ обновление подписок пользователя(так же используется для вставки) """
    return service.update_user_subscribes(user_id=user.id, subscribes_in=subscribes)
