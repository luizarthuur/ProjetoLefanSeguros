from core.configs import settings

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class TeamCarouselModel(settings.DBBaseModel):
    __tablename__ = 'team_carousel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    subtitulo = Column(String(100), nullable=True)
    nome = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    link1 = Column(String(255), nullable=True)
    link2 = Column(String(255), nullable=True)
    link3 = Column(String(255), nullable=True)
    nav_main_content_id = Column(Integer, ForeignKey('nav_main_content.id'))

    # Relacionamento com o modelo NavMainContent
    nav_main_content = relationship("NavMainContentModel", back_populates="team_carousels")
    