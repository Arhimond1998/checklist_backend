from datetime import timedelta

from fastapi import APIRouter, Depends, exceptions, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository, get_user_repository
from src.schemas import UserCreate, UserLogin, UserResponse, UserResponseLogin
from src.deps.database import get_db
from src.services.auth import auth_service
from src.deps.auth import check_token

router = APIRouter(prefix="/auth")


@router.get("/is_authorized", response_model=bool)
async def is_authorized(check_token=Depends(check_token)):
    return check_token


@router.post("/login", response_model=UserResponseLogin)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    await auth_service.authenticate_user(user_repo, user.login, user.password)
    user_db = await user_repo.get_by_login(user.login)
    if not user_db:
        raise exceptions.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=12)
    access_token = auth_service.create_access_token(
        data={"sub": user_db.login}, expires_delta=access_token_expires
    )
    await db.commit()
    return UserResponseLogin(
        id_user=user_db.id_user,
        name=user_db.name,
        surname=user_db.surname,
        patronymic=user_db.patronymic,
        mail=user_db.mail,
        login=user_db.login,
        access_token=access_token,
    )


@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user.password = auth_service.hash_password(user.password)
    new_user = await user_repo.create(user)
    await db.commit()
    return new_user
