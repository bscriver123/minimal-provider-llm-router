from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.deps.config import Settings, get_settings

API_KEY_NAME = "Authorization"


class OAuth2PasswordBearerWithHeader(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str, header_name: str):
        super().__init__(tokenUrl=tokenUrl)
        self.header_name = header_name

    async def __call__(self, request: Request):
        authorization: str = request.headers.get(self.header_name)
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = authorization[len("Bearer ") :]
        return token


oauth2_scheme = OAuth2PasswordBearerWithHeader(tokenUrl="token", header_name=API_KEY_NAME)


def authenticate_user(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> bool:
    if token != settings.app_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
