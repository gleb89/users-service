from typing import  NoReturn

from fastapi import status
from fastapi.responses import JSONResponse

from app.db.base import BaseRepository
from app.core.config import settings




class BasketsRepo(BaseRepository):
    collection_name = settings.mongodb_name_basket

    def __init__(
        self
    ) -> NoReturn:
        super().__init__()

    async def count_product_basket(
        self,
        user_id,
        product_id
        ):
        """
        Проверяет есть ли товар с полем product_id,
        при его наличии возвращает количество 
                                данного товара
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
        product = await db_collection.find_one(
            {
                "user_id" :user_id,
                'products.product_id':product_id
            }
            )
        if product:
            count_prod = [
                i['amount'] for i in product['products']
                if i['product_id'] == product_id][0]
            return count_prod
        else:
            return False


    async def add_product_basket(
        self,
        user_id,
        product_id
        ):
        """
        Добавление id товара в корзину
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
        user_basket  = await db_collection.find_one(
                            {
                                "user_id":user_id
                            }
                            )
        if user_basket:
            amount = await self.count_product_basket(
                user_id,
                product_id
                )
            if amount:
                amount +=1
                append_count_products = await db_collection.update_one(
                    {
                    'user_id':user_id,
                    'products.product_id':product_id
                    },
                    {'$set':
                        {
                        "products.$.amount" : amount
                        }
                    }
                )
            else:
                await db_collection.update_one(
                    {"user_id":user_id},
                            {'$push': 
                                {"products":{
                                    'product_id':product_id,
                                    'amount':1
                                }}
                    })
        else:
            await db_collection.insert_one(
                {'user_id':user_id,'products':[
                    {
                        'product_id':product_id,
                        'amount':1
                        }
                    ]
                    })
                
        basket_for_id_user = await db_collection.find_one(
                                        {
                                            "user_id":user_id
                                        }
                                    )
       
        return JSONResponse(
                    status_code = status.HTTP_201_CREATED,
                    content={
                        "status": "success",
                        "detail": None,
                        "payload": basket_for_id_user[
                                            'products'
                                            ],
                        }
                    )

    async def get_products_basket(
        self,
        user_id
        ):
        """
        Список id товаров добавленных в корзину
                                и их количество
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
       
        basket_for_id_user = await db_collection.find_one(
                                        {
                                            'user_id':user_id
                                        }
                                    )
        if basket_for_id_user:
            return JSONResponse(
                    content={
                        "status": "success",
                        "detail": None,
                        "payload": basket_for_id_user[
                                            'products'
                                            ],
                        }
                    )
        else:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "status": "failure",
                        "detail": "Not basket for user",
                        "payload": None,
                        }
                    )
       

    async def delete_products_basket(
        self,
        user_id,
        product_id
        ):
        """
        Удаление id товара из корзины
        """
        db_collection = self.get_mongo_collection(
            self.collection_name
            )
        basket_for_id_user = await db_collection.update_one(
                                    {"user_id":user_id},
                                    {'$pull': 
                                    {"products":{
                                    'product_id':product_id
                                    }
                                    }
                                    })
                                
        basket = await db_collection.find_one(
                            {
                                "user_id":user_id
                            }
                            )
        return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content={
                        
                        "status": "success",
                        "detail": None,
                        "payload": basket[
                                'products'
                                ],
                        }
                    )

