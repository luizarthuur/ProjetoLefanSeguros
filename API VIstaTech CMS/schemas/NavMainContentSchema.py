from typing import Optional, List

from pydantic import BaseModel as SCBaseModel
from schemas.TeamCarouselSchema import TeamCarouselSchema

class NavMainContentSchema(SCBaseModel):
    id: Optional[int]
    titulo_principal: str
    conteudo_principal: str
    team_carousels: List[TeamCarouselSchema] = []


    class Config:
        orm_mode = True