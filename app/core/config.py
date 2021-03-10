from pydantic import BaseSettings

from app.secretfirebase import *



class Settings(BaseSettings):
    SECRET_KEY = 'jdhfjhjei3ei87787383'
    service_name: str = "users"
    log_path: str = "/var/log"
    log_filename: str = "users.log"
    log_level: str = "info"
    log_rotation: str = "20 days"
    log_retention: str = "1 months"
    log_format: str = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    mongodb_dsn: str = "mongodb+srv://gleb:1234@cluster0.banrf.mongodb.net/test?retryWrites=true&w=majority"
    mongodb_dbname: str = "usersapp"
    mongodb_name_users :str = 'users'
    mongodb_name_favourites :str = 'favourites'
    mongodb_name_subscriptions :str = 'subscriptions'
    mongodb_name_basket :str = 'basket'
    mongo_max_connections: int = 1000
    mongo_min_connections: int = 10
    rmq_host: str = "127.0.0.1"


   
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "CONTRIB_"


settings: Settings = Settings()