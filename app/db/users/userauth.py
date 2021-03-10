from typing import Optional
from datetime import timedelta
from datetime import datetime

from fastapi.responses import JSONResponse

from jose import JWTError, jwt

from app.core.config import settings
from app.routers.profile import Users
from app.db.users.usersrepo import UsersRepository
from app.db.firebase import UserFirebase


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"



class UserClient(UserFirebase):
    def __init__(self):
        super().__init__()

    def virefity_phone(
        self,
        phone,
        text
        ):
        """
        Проверка наличия номера телефона в базе
        """
        try:
            user_phone = self.client.get_user_by_phone_number(
                phone
                )
        except:
            user_phone = None

        if text == "registration":
            """
            Если запрос на регистрацию
            """
            if not user_phone:
                return {
                    "status": "success",
                    "detail": None,
                    "payload": None
                    }
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "failure",
                        "detail": "this phone there is database",
                        "payload": None,
                    },
                )
        else:
            """
            Если запрос на вход
            """
            if user_phone:
                return {
                    "status": "success",
                    "detail": None,
                    "payload": {
                        "code": "23234234"
                        }
                }
            else:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "failure",
                        "detail": "this phone not in database",
                        "payload": None,
                    },
                )

    def create_access_token(
        self,
        user_uid: dict,
        expires_delta: Optional[timedelta] = None
        ):
        to_encode = user_uid.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update(
            {"exp": expire}
            )
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=ALGORITHM)
        return encoded_jwt

    def virefity_code(
        self,
        phone,
        code
        ):
        """
        Верификация кода для Firebase
        """
        
        
        try:
            verivy_phone_code = self.client.get_user_by_phone_number(
            phone
            )
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
                )
            access_token = self.create_access_token(
                    {"sub": str(verivy_phone_code.uid)},
                    expires_delta=access_token_expires
                    )
            return {
                "status": "success",
                "detail": None,
                "token_payload": {
                                "access_token": access_token,
                                "expiration_time":access_token_expires
                }   
                }
        except:
            return JSONResponse(
                        status_code=400,
                        content={
                            "status": "failure",
                            "detail": "code not verify",
                            "payload": None,
                        }
                    )


    def create(
        self,
        phone
        ):
        """
        Создание пользователя в Firebase
        """
        new_auth_user = self.client.create_user(
            phone_number=phone
            )
        user_id = new_auth_user.uid
        user = {
            "firebase_id": user_id,
            "phone_number": phone
            }
        try:
            response = {
                "status": "success",
                "detail": None,
                "payload": {
                "code": "434343"
                    }
                },
            return response, user  
        except:
            return JSONResponse(
                    status_code=400,
                    content={
                        "status": "failure",
                        "detail": "this phone registration in database",
                        "payload": None,
                    }
                ),None
