from typing import Optional,List
from datetime import datetime

from pydantic import BaseModel


#Users schemas
class VerifyPhone(BaseModel):
    phone: str

    class Config:

        schema_extra = {
            "example": {
                "phone": "+7 (900) 000 00 00",
            }
        }

class VerifyCode(BaseModel): 
    code:str
    phone: str

    class Config:

            schema_extra = {
            "example": {
                "code": "23234234",
                "phone": "+7 (900) 000 00 00",
            }
        }

class CreateUser(BaseModel):
    firebase_id:str
    phone_number: str



class UserUpdate(BaseModel):
    firebase_id:str
    email:Optional[str] = None
    first_name:str
    middle_name:str
    birthday: Optional[datetime]
    gender:str

    class Config:
        schema_extra = {
            "example": {
                "firebase_id": "JdVpwoBf2RQpThFMWFhFiNKAgwT2",
                "email": "example@mail.com",
                "first_name": "Иван",
                "middle_name": 'Михалыч',
                "birthday": '1952-07-10T00:00:00',
                "gender": 'male',
            }
        }



class UserInfo(BaseModel):
    phone_number: str
    email:Optional[str] = None
    first_name:str
    middle_name:str
    birthday: Optional[datetime]
    gender:str
    


# Favorites schemas
class Favorites(BaseModel):
    user_id:str
    products:List[str] = None



# Basket schemas
class Basket(Favorites):
    pass



# Subscriptions schemas
class Subscriptions(Favorites):
    pass

