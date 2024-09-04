from typing import Optional, List

from pydantic import BaseModel as SCBaseModel


from schemas.TeamCarouselSchema import TeamCarouselSchema 

class AddressComponentSchema(SCBaseModel):
    id: Optional[int]
    titulo: str
    endereco_conteudo: str
    telefone_conteudo: str
    email_conteudo: str



    class Config:
        orm_mode = True