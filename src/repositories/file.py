from pathlib import Path
from datetime import datetime
from uuid import uuid4

from fastapi import UploadFile, Depends
from src.deps.auth import get_current_user
from src.models import User

from src.core.config import settings


class FileRepository:
    def __init__(self, user: User):
        self.user = user
        self.user_path = f"{settings.UPLOAD_DIR}/{user.id_user}"

        path = Path(self.user_path)

        if not path.exists():
            path.mkdir()

    async def create(self, file: UploadFile) -> str:
        filename = f"{self.user.login}_{int(datetime.now().timestamp())}_{uuid4()}_.{file.filename.split('.')[-1]}"
        file_path = f"{self.user_path}/{filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return f"{settings.HOST_ADDRESS}/{file_path}"

    async def create_bunch(self, files: list[UploadFile]) -> list[str]:
        result = []
        for file in files:
            result.append(await self.create(file))
        return result


def get_file_repository(user: User = Depends(get_current_user)) -> FileRepository:
    return FileRepository(user)
