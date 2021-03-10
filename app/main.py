from fastapi import FastAPI
from fastapi_contrib.common.responses import UJSONResponse
from fastapi_contrib.db.utils import setup_mongodb

from app.middlewares import middleware
from app.routers.signin import users_signin
from app.routers.profile import users_profile
from app.routers.favourites_prod import favourites_products
from app.routers.basket_prod import basket_products 
from app.routers.subscriptions_prod import subscriptions_prod
from app.routers.signup import users_signup
from app.db.mongo_cls import mongo_db
from app.core.config import settings






tags_metadata = [{
    "name": "users",
    "description": "Сервис Регистрации и входа пользователей",
}]


app = FastAPI(
    title="Auth Profile",
    description="Документация API сервиса Входа\регистрации",
    version="3.0.0",
    openapi_url="/api/v3/users/openapi.json",
    docs_url="/api/v3/users/docs",
    openapi_tags=tags_metadata,
    default_response_class=UJSONResponse,
    middleware=middleware
)

app.include_router(
    users_signup,
    prefix="/signup",
    tags=["signup"],
    responses={404: {"description": "Not found"}})

app.include_router(
    users_signin,
    prefix="/signin",
    tags=["signin"],
    responses={404: {"description": "Not found"}})

app.include_router(
    users_profile,
    prefix="/profile",
    tags=["profile-users"],
    responses={404: {"description": "Not found"}})


app.include_router(
    favourites_products,
    prefix="/favourites",
    tags=["favourites-products"],
    responses={404: {"description": "Not found"}})


app.include_router(
    basket_products,
    prefix="/basket",
    tags=["basket-products"],
    responses={404: {"description": "Not found"}})

app.include_router(
    subscriptions_prod,
    prefix="/subscriptions",
    tags=["subscriptions-products"],
    responses={404: {"description": "Not found"}})


@app.on_event("startup")
async def startup():
    setup_mongodb(app)
    await mongo_db.connect()



@app.on_event("shutdown")
async def shutdown():
    await mongo_db.close_connection()
    
