from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.db.favourites.mongo_favorites import FavoritesRepository
from app.db.users import crud_token




favourites_products = APIRouter()


class Favorites(FavoritesRepository):
    def __init__(self):
        super().__init__()



@favourites_products.get(
    "/",
    status_code=200
    )
async def get_favorites_data(
    curent_user = Depends(crud_token.JWTBearer()),
    repo: FavoritesRepository = Depends(
        Favorites
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    по полученному uid возвращает  товаровы в 
                                        избранном
    """
    try:
        favourites_products = await repo.get_products_favorites(
            curent_user
            )
        return favourites_products 
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )


@favourites_products.post(
    "/{product_id}"
    )
async def update_profile_data(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: FavoritesRepository = Depends(
        Favorites
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Добавляет id товара в избранное относящееся
                                к uid пользователя                         
    """
    try:
        favourites_products = await repo.add_product_favorites(
            curent_user,
            product_id
            )
        return favourites_products
    except:
        return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "failure",
                            "detail": "HTTP_401_UNAUTHORIZED",
                            "payload": None,
                        }
                    )



@favourites_products.delete(
    "/{product_id}"
    )
async def delete_product(
    product_id:str,
    curent_user = Depends(crud_token.JWTBearer()),
    repo: FavoritesRepository = Depends(
        Favorites
        )
):
    """
    Информация:
    - **curent_user**:Проверка Bearer токена
                        возвращает uid user
    - **product_id**:id товара
    - **Описание**:   Принимает Bearer токен
    при успехе возвращает uid профиля пользователя,
    Удаляет id товара из избранного относящегося
                                к uid пользователя                         
    """
    try:
        delete_resp = await repo.delete_products_favorites(
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

