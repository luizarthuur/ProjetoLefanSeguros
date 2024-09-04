from typing import Optional, List

from pydantic import BaseModel as SCBaseModel



from schemas.AddressComponentSchema import AddressComponentSchema
from schemas.ContentSectionSchema import ContentSectionSchema
from schemas.InfoMainContentSchema import InfoMainContentSchema
from schemas.NavMainContentSchema import NavMainContentSchema
from schemas.TeamCarouselSchema import TeamCarouselSchema
from schemas.VideoContentSchema import VideoContentSchema

#Remover o opcional quando acabar os testes, pois será tudo obrigatório

class CompositeSchemas(SCBaseModel):
    address_component: Optional[AddressComponentSchema]
    content_section: Optional[ContentSectionSchema]
    info_main_content: Optional[InfoMainContentSchema]
    nav_main_content: Optional[NavMainContentSchema]
    team_carousel: Optional[List[TeamCarouselSchema]]  # Lista de TeamCarouselSchema, se houver múltiplos itens
    video_content: Optional[VideoContentSchema]


    class Config:
        orm_mode = True