from fastapi import APIRouter, Depends

from app.db.users.usersrepo import UsersRepository
from app.schemas import schemas
from app.db.users.userauth import UserClient
from app.routers.profile import UsersRepository, Users



users_signup = APIRouter()



class PhoneAuth(UserClient):
    """Обертка над UserClient 
    """
    def __init__(self):
        super().__init__()

  

@users_signup.post(
    '/check_phone',
    status_code=200
    )
def verification_phone(
    phone:schemas.VerifyPhone,
    repo: UserClient= Depends(PhoneAuth)):
    """
    Информация:
    - **phone**:Номер телефона пользователя
    - **Описание**: По введеннному параметру
        phone обращаемся к Firebase и проверяем 
        наличие данного номера в базе 
        зарегестрированных пользователей
    """
    virefity = repo.virefity_phone(
        phone.phone,
        text='registration'
        )
    return virefity



@users_signup.post(
    '/',
    status_code=200
    )
async def registration_user(
    phone:schemas.VerifyPhone,
    repo: UserClient= Depends(PhoneAuth),
    mongo_user: UsersRepository = Depends(Users)):
    """
    Информация:
    - **phone**:Номер телефона пользователя
    - **Описание**: По введеннному параметру
        phone регистрируем пользователя в 
        Firebase и отправляем код верификации 
                            на данный номер
    """
    
    new_user_auth, data_user = repo.create(
        phone.phone
        )
    if data_user:
        await mongo_user.create_new_user(
            data_user
            )
    return new_user_auth


@users_signup.post(
    '/check_code',
    status_code=200
    )
def check_code_phone(
    phone_code:schemas.VerifyCode,
    repo: UserClient= Depends(PhoneAuth)):
    """
    Информация:
    - **phone**:Номер телефона пользователя
    - **code**:Код верификации пользователя
    - **Описание**: По введеннному параметру
        phone и code обращаемся к Firebase,
        для проверки кода 
    """
    virefity_code = repo.virefity_code(
        phone_code.phone,
        phone_code.code
        )
    return virefity_code