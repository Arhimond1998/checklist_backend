import argon2

from src.repositories.user import UserRepository

ph = argon2.PasswordHasher()


class AuthService:
    async def login(user_repopsitory: UserRepository, login, password):
        password_hash = await user_repopsitory.get_password_hash_for_user(login)

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


auth_service = AuthService()
