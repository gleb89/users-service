from typing import List, Dict, Optional, NoReturn

from motor.motor_asyncio import AsyncIOMotorCollection

from app.core.config import settings
from app.db.mongo_cls import mongo_db



class BaseRepository:
    mongo_databese_name: str = settings.mongodb_dbname

    def __init__(self) -> NoReturn:
        self.mongo = mongo_db.get_mongo()

    def get_mongo_collection(self,collection_name) -> AsyncIOMotorCollection:
        name: str = self.collection_name
        return self.mongo[self.mongo_databese_name][name]

        
        

