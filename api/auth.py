from fastapi import APIRouter, Depends
from schemas import UserOut, UserIn, Token
from services.auth import AuthService, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/auth')


@router.post('/sign-up', response_model=Token)
def sign_up(user_data: UserIn,
            service: AuthService = Depends()
            ):
    """ регистрация пользователя """
    return service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(),
            service: AuthService = Depends(),
            ):
    """ аутентификация пользователя """
    return service.authenticate_user(form_data.username, form_data.password)


@router.get('/me', response_model=UserOut)
def get_user(user: UserOut = Depends(get_current_user)):
    return user
