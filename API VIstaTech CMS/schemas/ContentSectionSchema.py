from typing import Optional

from pydantic import BaseModel as SCBaseModel

class ContentSectionSchema(SCBaseModel):
    id: Optional[int]
    titulo: str
    conteudo: str



    class Config:
        orm_mode = True