import asyncio
import os

from alembic.config import Config

from src.core.config import settings

from logging import getLogger

logger = getLogger(__name__)


async def init_migration():

    try:
        logger.debug("migration start")
        config_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), os.path.pardir, "alembic.ini"
        )
        alembic_cfg = Config(config_path)
        from alembic import command

        command.upgrade(alembic_cfg, "head")
        logger.debug("migration finish")
    except Exception as e:
        logger.error(str(e))

