from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.db.basket.mongo_basket import BasketsRepo
from app.db.users import crud_token


basket_products = APIRouter()


class Baskets(BasketsRepo):
    def __init__(self):
        super().__init__()



@basket_products.get(
    "/",
    status_code=200
    )
async def get_basket_data(
    curent_user = Depends(crud_token.JWTBearer()),
    repo: BasketsRepo = Depends(
        Baskets
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    по полученному uid возвращает  товарвы и 
                    их количество в корзине
                                        
    """
    try:
        subscriptions_prod = await repo.get_products_basket(
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


@basket_products.post(
    "/{product_id}"
    )
async def update_basket_data(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: BasketsRepo = Depends(
        Baskets
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Добавляет id товара в корзину относящуюся
                                к uid пользователя                         
    """
    try:
        subscriptions_prod = await repo.add_product_basket(
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



@basket_products.delete(
    "/{product_id}"
    )
async def delete_product(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: BasketsRepo = Depends(
        Baskets
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Удаляет id товара из корзины относящейся
                                к uid пользователя                         
    """
    try:
        delete_resp = await repo.delete_products_basket(
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
