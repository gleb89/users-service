from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Request

from jose import JWTError, jwt

from app.core.config import settings
from app.db.users.usersrepo import UsersRepository


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




class JWTBearer(HTTPBearer):

    def __init__(
        self,
        auto_error: bool = True
        ):
        super(
            JWTBearer,
            self).__init__(
            auto_error=auto_error
            )

    async def __call__(
        self, request: Request
        ):
        credentials: HTTPAuthorizationCredentials = await super(
                            JWTBearer, self
                            ).__call__(
                                request
                                )
        
        if credentials:
            return await self.get_current_user(credentials.credentials)
   

    async def get_current_user(
        self,
        token: str 
        ):
        try:
            payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM])
            uid = payload.get(
            "sub"
            )
            return uid
        
        except JWTError:
            return JWTError






