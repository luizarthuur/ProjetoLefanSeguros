from typing import Optional

from pydantic import BaseModel as SCBaseModel

class VideoContentSchema(SCBaseModel):
    id: Optional[int]
    titulo: str
    video_link: str


    class Config:
        orm_mode = True