from datetime import datetime, timezone, timedelta
from functools import wraps
import argon2
from jose import jwt

from fastapi import HTTPException
from src.repositories.user import UserRepository
from src.core.config import settings

ph = argon2.PasswordHasher()


class AuthService:
    @staticmethod
    def check_roles(roles: list[str]):
        """
        Декоратор на проверку доступных  компонент
        """

        def decorator(func):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                headers = kwargs.get("request").headers
                token = headers["Authorization"].split(" ")[-1]
                data = AuthService.decode_access_token(token)
                user_roles = data['roles']
                if len(set(user_roles) & set(roles)) == 0:
                    raise HTTPException(
                        status_code=403, detail="У вас нет прав доступа"
                    )
                res = await func(*args, **kwargs)
                return res

            return wrapped

        return decorator

    @staticmethod
    def my_decorator(func):
        @wraps(func)  # Apply @wraps to the wrapper function
        async def wrapper(*args, **kwargs):
            print("Before calling the function.")
            result = await func(*args, **kwargs)
            print("After calling the function.")
            return result

        return wrapper

    async def authenticate_user(
        self, user_repopsitory: UserRepository, login: str, password: str
    ):
        password_hash = await user_repopsitory.get_password_hash_for_user(login)

        if not password_hash:
            return False

        # Verify password, raises exception if wrong.
        try:
            ph.verify(password_hash, password)
        except argon2.VerifyMismatchError:
            return False
        except Exception as e:
            print(e)

        # Now that we have the cleartext password,
        # check the hash's parameters and if outdated,
        # rehash the user's password in the database.
        if ph.check_needs_rehash(password_hash):
            await user_repopsitory.set_password_hash_for_user(login, ph.hash(password))

        return True

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    def hash_password(self, password: str):
        return ph.hash(password)


auth_service = AuthService()
