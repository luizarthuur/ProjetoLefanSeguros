from core.configs import settings

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class AddressComponentModel(settings.DBBaseModel):
    __tablename__ = 'address_component'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(Text, nullable=False)
    endereco_conteudo = Column(Text, nullable=True)
    telefone_conteudo = Column(String(50), nullable=True)
    email_conteudo = Column(String(150), nullable=True)
