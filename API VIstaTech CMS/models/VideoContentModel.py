from core.configs import settings

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class VideoContentModel(settings.DBBaseModel):
    __tablename__ = 'video_content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    video_link = Column(String(255), nullable=False)
