from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class CompositeModel(settings.DBBaseModel):
    __tablename__ = 'composite'
    id = Column(Integer, primary_key=True, autoincrement=True)
