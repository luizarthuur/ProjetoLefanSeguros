from core.configs import settings

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class ContentSectionModel(settings.DBBaseModel):
    __tablename__ = 'content_section'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    conteudo = Column(Text, nullable=True)
