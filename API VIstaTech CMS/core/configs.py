from pydantic import BaseSettings

from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    '''
    Configurações gerais da aplicação
    '''

    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:vistatech3011@localhost:5432/lefanseguros-teste1"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True
        arbitrary_types_allowed = True

settings = Settings()