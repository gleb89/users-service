from fastapi import APIRouter, Depends

from app.db.users.userauth import UserClient
from app.routers.signup import PhoneAuth
from app.db.users import crud_token
from app.schemas.schemas import UserInfo, VerifyPhone,\
                                        VerifyCode
from app.db.users.usersrepo import UsersRepository


users_signin = APIRouter()


@users_signin.post(
    "/check_phone",
    status_code=200
    )
def verification_phone(
    phone:VerifyPhone,
    repo: UserClient = Depends(PhoneAuth)):
    """
    Информация:
    - **phone**:Номер телефона пользователя
    - **Описание**: По введеннному параметру
        phone обращаемся к Firebase и проверяем наличие
        предоставленного номера телефона пользователем,
        присутствие номера в Firebase,означает ,что
        пользователь зарегистрирован в системе,jfirebase
        отправляет код верификации на номер(phone)
    """
    virefity_phone = repo.virefity_phone(
        phone.phone,
        text="auth"
        )
    return virefity_phone




@users_signin.post(
    '/check_code',
    status_code=200
    )
def check_code_phone(
    phone_code:VerifyCode,
    repo: UserClient= Depends(PhoneAuth)):
    """
    Информация:
    - **phone**:Номер телефона пользователя
    - **code**:Код верификации пользователя
    - **Описание**: По введеннному параметру
        phone и code обращаемся к Firebase,
        в случае успеха отправляем на 
        клиентскую часть access_token 
    """
    virefity_code = repo.virefity_code(
        phone_code.phone,
        phone_code.code
        )
    return virefity_code




