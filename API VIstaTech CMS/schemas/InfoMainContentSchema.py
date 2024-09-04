from typing import Optional

from pydantic import BaseModel as SCBaseModel

class InfoMainContentSchema(SCBaseModel):
    id: Optional[int]
    titulo_principal: str
    conteudo_principal: str


    class Config:
        orm_mode = True