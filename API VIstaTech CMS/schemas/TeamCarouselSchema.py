from typing import Optional

from pydantic import BaseModel as SCBaseModel

class TeamCarouselSchema(SCBaseModel):
    id: Optional[int]
    titulo: str
    subtitulo: str
    nome: str
    cargo: str
    descricao: str
    link1: str
    link2: str
    link3: str
    nav_main_content_id: Optional[int] 



    class Config:
        orm_mode = True