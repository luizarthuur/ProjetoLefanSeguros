from core.configs import settings

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class NavMainContentModel(settings.DBBaseModel):
    __tablename__ = 'nav_main_content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo_principal = Column(String(100), nullable=False)
    conteudo_principal = Column(Text, nullable=True)
    team_carousels = relationship("TeamCarouselModel", back_populates="nav_main_content", lazy='selectin')
    
