from typing import Annotated

from jose import jwt, exceptions
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.core.config import settings
from src.repositories.user import UserRepository, get_user_repository

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


async def get_current_user(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)], token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except exceptions.InvalidTokenError:
        raise credentials_exception
    user = await user_repo.get_by_login(login)
    if user is None:
        raise credentials_exception
    return user


async def check_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except exceptions.InvalidTokenError:
        raise credentials_exception
    return True
