from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.schemas import schemas
from app.db.users.usersrepo import UsersRepository
from app.db.users import crud_token


users_profile = APIRouter()


class Users(UsersRepository):
    """Обертка над UsersRepository"""

    def __init__(self) -> None:
        super().__init__()



@users_profile.get(
    "/",
    status_code=200
    )
async def get_profile_data(
    curent_user = Depends(crud_token.JWTBearer()),
    repo: UsersRepository = Depends(
        Users
        )
    ):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **Описание**:  Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    по полученному uid возвращает items пользователя
    """
    try:
        user_data = await repo.verify_user_data(
            curent_user
            )
        return user_data
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )


@users_profile.put(
    "/",
    status_code=201
    )
async def update_profile_data(
    user_data: schemas.UserUpdate,
    repo: UsersRepository = Depends(Users)
):
    """
    Информация:
    - **user_data**:Pydantic schema c полями:
        (email,first_name,middle_name,birthday,
                            gender,firebase_id)
    - **Описание**: Находит профиль в Mongodb по полю
        firebase_id,добавляет данные из полей - user_data
    """
    user_update = await repo.update_user(
        user_data
        )
    
    return user_update
