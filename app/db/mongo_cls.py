from typing import NoReturn
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoDB:
    mongodb_dsn: str = settings.mongodb_dsn
    max_pool_size: int = settings.mongo_max_connections
    min_pool_size: int = settings.mongo_min_connections

    client: AsyncIOMotorClient

    def get_mongo(
        self,
    ) -> AsyncIOMotorClient:
        return self.client

    async def connect(
        self,
    ) -> NoReturn:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            self.mongodb_dsn,
            maxPoolSize=self.max_pool_size,
            minPoolSize=self.min_pool_size)

    async def close_connection(
        self,
    ) -> NoReturn:
        self.client.close()

mongo_db: MongoDB = MongoDB()