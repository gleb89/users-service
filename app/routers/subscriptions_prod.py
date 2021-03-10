from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.db.subscriptions.mongo_subscr import SubscriptionsRepo
from app.db.users import crud_token
from app.schemas import schemas

subscriptions_prod = APIRouter()


class Subscriptions(SubscriptionsRepo):
    def __init__(self):
        super().__init__()



@subscriptions_prod.get(
    "/",
    status_code=200
    )
async def get_favorites_data(
    curent_user = Depends(crud_token.JWTBearer()),
    repo: SubscriptionsRepo = Depends(
        Subscriptions
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    по полученному uid возвращает  товары в 
                                    подписках
    """
    try:
        subscriptions_prod = await repo.get_products_subscriptions(
            curent_user
            )
        return subscriptions_prod 
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )


@subscriptions_prod.post(
    "/{product_id}"
    )
async def update_profile_data(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: SubscriptionsRepo = Depends(
        Subscriptions
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Добавляет id товара в подписки относящиеся
                                к uid пользователя                         
    """
    try:
        subscriptions_prod = await repo.add_product_subscriptions(
            curent_user,
            product_id
            )
        return subscriptions_prod
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )



@subscriptions_prod.delete(
    "/{product_id}"
    )
async def delete_product(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: SubscriptionsRepo = Depends(
        Subscriptions
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Удаляет id товара из подписок относящихся
                                к uid пользователя                         
    """
    try:
        delete_resp = await repo.delete_products_subscriptions(
            curent_user,
            product_id
            )
        return delete_resp
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )


