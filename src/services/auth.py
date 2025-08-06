from datetime import datetime, timezone, timedelta

import argon2
from jose import jwt

from src.repositories.user import UserRepository
from src.core.config import settings

ph = argon2.PasswordHasher()


class AuthService:
    async def authenticate_user(self, user_repopsitory: UserRepository, login: str, password: str):
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
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def hash_password(self, password: str):
        return ph.hash(password)

auth_service = AuthService()
