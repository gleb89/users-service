from typing import  NoReturn

from fastapi import status
from fastapi.responses import JSONResponse

from app.db.base import BaseRepository
from app.core.config import settings




class SubscriptionsRepo(BaseRepository):
    collection_name = settings.mongodb_name_subscriptions

    def __init__(
        self
    ) -> NoReturn:
        super().__init__()


    async def add_product_subscriptions(
        self,
        user_id,
        product_id
        ):
        """
        Добавление id товара в подписки
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
        user_subscriptions  = await db_collection.find_one(
                            {
                                "user_id":user_id
                            }
            )
        if user_subscriptions:
            await db_collection.update_one(
                {"user_id":user_id},
                            {'$push': 
                {"products":product_id}
                }
                )
        else:
            await db_collection.insert_one(
                {'user_id':user_id,'products':[product_id]}
                )
        subscriptions_for_id_user = await db_collection.find_one(
            {"user_id":user_id}
            )
        
        return JSONResponse(
                    status_code = status.HTTP_201_CREATED,
                    content={
                        "status": "success",
                        "detail": None,
                        "payload": subscriptions_for_id_user['products'],
                        }
                    )

    async def get_products_subscriptions(
        self,
        user_id
        ):
        """
        Список id товаров добавленных в подписках
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
       
        subscriptions_for_id_user = await db_collection.find_one(
            {'user_id':user_id}
            )
        if subscriptions_for_id_user:
            return JSONResponse(
                    content={
                        "status": "success",
                        "detail": None,
                        "payload": subscriptions_for_id_user['products'],
                        }
                    )
        else:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "status": "failure",
                        "detail": "Not subscriptions for user",
                        "payload": None,
                        }
                    )
       

    async def delete_products_subscriptions(
        self,
        user_id,
        product_id
        ):
        """
        Удаление id товара из подписок
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
        subscriptions_for_id_user = await db_collection.update_one(
                                {'user_id':user_id },{
                                '$pull': 
                                {'products':product_id}
                                }
                                )
        subscriptions = await db_collection.find_one(
                            {"user_id":user_id}
                            )
        return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content={
                        
                        "status": "success",
                        "detail": None,
                        "payload": subscriptions[
                            'products'
                            ],
                        }
                    )

