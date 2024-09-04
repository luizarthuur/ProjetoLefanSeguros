from core.configs import settings
from core.database import engine

from models.TeamCarouselModel import TeamCarouselModel

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def create_tables() -> None:
    import models.__all_models
    print('Criando Tabelas...')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(TeamCarouselModel.metadata.create_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

    print('Tabelas Criadas com Sucesso')

if __name__ == '__main__':

    import asyncio

    asyncio.run(create_tables())