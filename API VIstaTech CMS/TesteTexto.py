'''from typing import List
from fastapi import APIRouter
from core.deps import get_session

from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.AddressComponentModel import AddressComponentModel
from models.BackgroundImageModel import BackgroundImageModel
from models.CarouselPropagandaModel import CarouselPropagandaModel
from models.ContentSectionModel import ContentSectionModel
from models.InfoMainContentModel import InfoMainContentModel
from models.LogoModel import LogoModel
from models.NavMainContentModel import NavMainContentModel
from models.TeamCarouselModel import TeamCarouselModel
from models.VideoContentModel import VideoContentModel

from schemas.AddressComponentSchema import AddressComponentSchema
from schemas.BackgroundImageSchema import BackgroundImageSchema
from schemas.CarouselPropagandaSchema import CarouselPropagandaSchema
from schemas.ContentSectionSchema import ContentSectionSchema
from schemas.InfoMainContentSchema import InfoMainContentSchema
from schemas.LogoSchema import LogoSchema
from schemas.NavMainContentSchema import NavMainContentSchema
from models.TeamCarouselModel import TeamCarouselModel
from models.VideoContentModel import VideoContentModel

#Verificar todos os models e schemas novamente
#Fazer o Crud para cada parte do website

router = APIRouter()

# POST URL LOGO - Responsabilidade de IMAGENS

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LogoSchema)
async def post_logo(logo: LogoSchema, db: AsyncSession = Depends(get_session)):
    
    nova_logo = LogoModel(logo_url = logo.logo_url)

    db.add(nova_logo)
    await db.commit()
    await db.refresh(nova_logo)

    return nova_logo

#Teste GET

@router.get('/', response_model=List[LogoSchema])
async def get_logo(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LogoModel)
        result = await session.execute(query)
        logos: List[LogoModel] = result.scalars().all()

    return logos
    
#GET por ID

@router.get('/{logo_id}', response_model=LogoSchema, status_code=status.HTTP_200_OK)
async def getLogo(logo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:

        query = select(LogoModel).filter(LogoModel.id == logo_id)
        result = await session.execute(query)
        logo = result.scalar_one_or_none()

        if logo:
            return logo
        else:
            raise HTTPException(detail='URL da logo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

#PUT por ID
         
@router.put('/{logo_id}', response_model=LogoSchema, status_code=status.HTTP_202_ACCEPTED)
async def putLogo(logo_id:int, logo: LogoSchema, db: AsyncSession= Depends(get_session)):

    async with db as session:
        
        query = select(LogoModel).filter(LogoModel.id == logo_id)
        result = await session.execute(query)
        logo_up = result.scalar_one_or_none()

        if logo_up:
            logo_up.logo_url = logo.logo_url

            await session.commit()

            return logo_up
        
        else:
            raise HTTPException(detail='URL da logo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE por ID

@router.delete('/{logo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delLogo(logo_id: int, db: AsyncSession= Depends(get_session)):

    async with db as session:

        query = select(LogoModel).filter(LogoModel.id == logo_id)
        result = await session.execute(query)
        logo_del = result.scalar_one_or_none()

        if logo_del:
            await session.delete(logo_del)

            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
                raise HTTPException(detail='URL da logo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
'''