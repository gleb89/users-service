from typing import  NoReturn

from fastapi.responses import JSONResponse

from app.db.base import BaseRepository
from app.core.config import settings
from app.schemas import schemas



class UsersRepository(BaseRepository):
    collection_name = settings.mongodb_name_users

    def __init__(
        self,
        # rabbitmq: RabbitMQ,
    ) -> NoReturn:
        super().__init__()

        # self.rabbitmq = rabbitmq

    async def create_new_user(
        self,
        user
        ):
        """
        Создание пользователя в Mongodb
        с полями взятыми из Firebase пользователя
        phone_number ,firebase_id
        """
        db_collection = self.get_mongo_collection(self.collection_name)
        return db_collection.insert_one(user)

    async def update_user(
        self,
        user_data
        ):
        """
        Добавление данных пользователя Mongodb
        """
        try:
            db_collection = self.get_mongo_collection(self.collection_name)
            user_update = await db_collection.update_one(
                {"firebase_id": user_data.firebase_id},
                {
                    "$set": {
                        "email": user_data.email,
                        "first_name": user_data.first_name,
                        "middle_name": user_data.middle_name,
                        "birthday": user_data.birthday,
                        "gender": user_data.gender,
                    }
                },
            )
            user_data_new = await db_collection.find_one(
                {"firebase_id": user_data.firebase_id}
            )
            user = schemas.UserInfo(
                **user_data_new
                )
            return {
                "status": "success",
                "detail": None,
                "payload": user
                }
        except:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "failure",
                    "detail": "not id in database",
                    "payload": None,
                },
            )

    async def get_user(
        self,
        firebase_id
        ):
        """
        Вывод информации об пользователе по его
                                    firebase_id
        """
        try:
            db_collection = self.get_mongo_collection(self.collection_name)
            user_db = await db_collection.find_one(
                {
                    "firebase_id": firebase_id
                    }
                    )
            user = schemas.UserInfo(**user_db)
            return {
                "status": "success",
                "detail": None,
                "payload": user
                }
        except:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "failure",
                    "detail": "not id in database",
                    "payload": None,
                },
            )

    async def verify_user_data(
        self,firebase_id
        ):
        """
        Вывод информации об пользователе по его
                                    Bearer Token
        """
        db_collection = self.get_mongo_collection(self.collection_name)
        user_data = await db_collection.find_one(
                {"firebase_id": firebase_id}
            )
        user = schemas.UserInfo(
            **user_data
            )
        return user


