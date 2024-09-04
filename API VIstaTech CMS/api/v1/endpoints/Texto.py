from typing import List
from fastapi import APIRouter, HTTPException, Path
from core.deps import get_session
from sqlalchemy import desc

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.CompositeSchemas import CompositeSchemas


from models.AddressComponentModel import AddressComponentModel
from models.ContentSectionModel import ContentSectionModel
from models.InfoMainContentModel import InfoMainContentModel
from models.NavMainContentModel import NavMainContentModel
from models.TeamCarouselModel import TeamCarouselModel
from models.VideoContentModel import VideoContentModel

from schemas.TeamCarouselSchema import TeamCarouselSchema


router = APIRouter()



# POST Todo o texto do website
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CompositeSchemas)
async def post_texto(data: CompositeSchemas, db: AsyncSession = Depends(get_session)):
    address_component = AddressComponentModel(
        titulo=data.address_component.titulo,
        endereco_conteudo=data.address_component.endereco_conteudo,
        telefone_conteudo=data.address_component.telefone_conteudo,
        email_conteudo=data.address_component.email_conteudo
    )

    content_section = ContentSectionModel(
        titulo=data.content_section.titulo,
        conteudo=data.content_section.conteudo
    )

    info_main_content = InfoMainContentModel(
        titulo_principal=data.info_main_content.titulo_principal,
        conteudo_principal=data.info_main_content.conteudo_principal
    )

    nav_main_content = NavMainContentModel(
        titulo_principal=data.nav_main_content.titulo_principal,
        conteudo_principal=data.nav_main_content.conteudo_principal
    )

    video_content = VideoContentModel(
        titulo=data.video_content.titulo,
        video_link=data.video_content.video_link
    )

    # Adicionando os componentes e seções
    db.add(address_component)
    db.add(content_section)
    db.add(info_main_content)
    db.add(nav_main_content)
    db.add(video_content)

    await db.commit()

    await db.refresh(nav_main_content)

    # Adicionando os carrosséis com referência ao nav_main_content_id
    # Criar e adicionar múltiplos itens de TeamCarousel

    await db.commit()

    await db.refresh(address_component)
    await db.refresh(content_section)
    await db.refresh(info_main_content)
    await db.refresh(nav_main_content)
    await db.refresh(video_content)

    nav_main_content = await db.execute(
    select(NavMainContentModel)
    .filter_by(titulo_principal=data.nav_main_content.titulo_principal)
    .order_by(desc(NavMainContentModel.id))  # Substitua 'data_de_criacao' pelo campo de ordenação desejado
)

    # Pega o primeiro resultado da lista ordenada
    nav_main_content = nav_main_content.scalars().first()

    if not nav_main_content:
        raise HTTPException(status_code=404, detail="NavMainContent not found")

    # Agora você pode adicionar os itens do carrossel associando o nav_main_content.id
    for carousel_item in data.team_carousel:
        team_carousel = TeamCarouselModel(
            titulo=carousel_item.titulo,
            subtitulo=carousel_item.subtitulo,
            nome=carousel_item.nome,
            cargo=carousel_item.cargo,
            descricao=carousel_item.descricao,
            link1 = carousel_item.link1,
            link2 = carousel_item.link2,
            link3 = carousel_item.link3,
            nav_main_content_id=nav_main_content.id  # Associando com o ID de NavMainContent
        )
        db.add(team_carousel)

    await db.commit()

    return {
        "address_component": address_component,
        "content_section": content_section,
        "info_main_content": info_main_content,
        "nav_main_content": nav_main_content,
        "video_content": video_content,
        "team_carousel": [carousel_item for carousel_item in data.team_carousel]   
    }


#GET por ID

@router.get('/{id}', response_model=CompositeSchemas, status_code=status.HTTP_200_OK)
async def get_composite_data(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        # Obter os dados de AddressComponentModel
        address_query = select(AddressComponentModel).filter(AddressComponentModel.id == id)
        address_result = await session.execute(address_query)
        address_component = address_result.scalar_one_or_none()

        # Obter os dados de ContentSectionModel
        content_query = select(ContentSectionModel).filter(ContentSectionModel.id == id)
        content_result = await session.execute(content_query)
        content_section = content_result.scalar_one_or_none()

        # Obter os dados de InfoMainContentModel
        info_query = select(InfoMainContentModel).filter(InfoMainContentModel.id == id)
        info_result = await session.execute(info_query)
        info_main_content = info_result.scalar_one_or_none()

        # Obter os dados de NavMainContentModel
        nav_query = select(NavMainContentModel).filter(NavMainContentModel.id == id)
        nav_result = await session.execute(nav_query)
        nav_main_content = nav_result.scalar_one_or_none()

        # Obter os dados de TeamCarouselModel (supondo que nav_main_content_id seja usado para ligação) - Excluido pois estava retornando duas vezes devido a NavMainContentModel
        #carousel_query = select(TeamCarouselModel).filter(TeamCarouselModel.nav_main_content_id == nav_main_content.id)
        #carousel_result = await session.execute(carousel_query)
        #team_carousel = carousel_result.scalars().all()  # Pode retornar vários itens

        # Obter os dados de VideoContentModel
        video_query = select(VideoContentModel).filter(VideoContentModel.id == id)
        video_result = await session.execute(video_query)
        video_content = video_result.scalar_one_or_none()

        if address_component is None and content_section is None and info_main_content is None and nav_main_content is None and video_content is None:
            raise HTTPException(detail='Nenhum dado encontrado para o ID fornecido', status_code=status.HTTP_404_NOT_FOUND)

        if address_component or content_section or info_main_content or nav_main_content or '''team_carousel''' or video_content:
            return CompositeSchemas(
                address_component=address_component,
                content_section=content_section,
                info_main_content=info_main_content,
                nav_main_content=nav_main_content,
                #team_carousel=team_carousel,
                video_content=video_content
            )
        


        else:
            raise HTTPException(detail='Nenhum dado encontrado para o ID fornecido', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=CompositeSchemas, status_code=status.HTTP_200_OK)
async def update_composite_data(
    id: int,
    data: CompositeSchemas,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        address_component = content_section = info_main_content = nav_main_content = video_content = None
        existing_carousels = []

        # Atualizar AddressComponentModel
        if data.address_component:
            address_query = select(AddressComponentModel).filter(AddressComponentModel.id == id)
            address_result = await session.execute(address_query)
            address_component = address_result.scalar_one_or_none()

            if address_component:
                for key, value in data.address_component.dict(exclude_unset=True).items():
                    setattr(address_component, key, value)
                await session.commit()

        # Atualizar ContentSectionModel
        if data.content_section:
            content_query = select(ContentSectionModel).filter(ContentSectionModel.id == id)
            content_result = await session.execute(content_query)
            content_section = content_result.scalar_one_or_none()

            if content_section:
                for key, value in data.content_section.dict(exclude_unset=True).items():
                    setattr(content_section, key, value)
                await session.commit()

        # Atualizar InfoMainContentModel
        if data.info_main_content:
            info_query = select(InfoMainContentModel).filter(InfoMainContentModel.id == id)
            info_result = await session.execute(info_query)
            info_main_content = info_result.scalar_one_or_none()

            if info_main_content:
                for key, value in data.info_main_content.dict(exclude_unset=True).items():
                    setattr(info_main_content, key, value)
                await session.commit()

        # Atualizar NavMainContentModel
        if data.nav_main_content:
            nav_query = select(NavMainContentModel).filter(NavMainContentModel.id == id)
            nav_result = await session.execute(nav_query)
            nav_main_content = nav_result.scalar_one_or_none()

            if nav_main_content:
                for key, value in data.nav_main_content.dict(exclude_unset=True).items():
                    setattr(nav_main_content, key, value)
                await session.commit()

        # Atualizar VideoContentModel
        if data.video_content:
            video_query = select(VideoContentModel).filter(VideoContentModel.id == id)
            video_result = await session.execute(video_query)
            video_content = video_result.scalar_one_or_none()

            if video_content:
                for key, value in data.video_content.dict(exclude_unset=True).items():
                    setattr(video_content, key, value)
                await session.commit()

        # Atualizar TeamCarouselModel
        if data.team_carousel:
            # Buscamos todos os carrosséis associados ao conteúdo principal
            carousels_query = select(TeamCarouselModel).filter(TeamCarouselModel.nav_main_content_id == id)
            carousels_result = await session.execute(carousels_query)
            existing_carousels = carousels_result.scalars().all()

            # Atualizar ou criar carrosséis
            for idx, carousel_item in enumerate(data.team_carousel):
                if idx < len(existing_carousels):
                    # Atualiza carrosséis existentes
                    carousel = existing_carousels[idx]
                    for key, value in carousel_item.dict(exclude_unset=True).items():
                        setattr(carousel, key, value)
                    carousel.nav_main_content_id = id
                else:
                    # Adiciona novos carrosséis
                    new_carousel = TeamCarouselModel(
                        titulo=carousel_item.titulo,
                        subtitulo=carousel_item.subtitulo,
                        nome=carousel_item.nome,
                        cargo=carousel_item.cargo,
                        descricao=carousel_item.descricao,
                        link1=carousel_item.link1,
                        link2=carousel_item.link2,
                        link3=carousel_item.link3,
                        nav_main_content_id=id
                    )
                    session.add(new_carousel)
            
            await session.commit()

        # Verifica se todas as entidades são None
        if address_component is None and content_section is None and info_main_content is None and nav_main_content is None and video_content is None and not existing_carousels:
            raise HTTPException(status_code=404, detail="ID não encontrado.")

        # Retornar os dados atualizados
        return CompositeSchemas(
            address_component=data.address_component,
            content_section=data.content_section,
            info_main_content=data.info_main_content,
            nav_main_content=data.nav_main_content,
            video_content=data.video_content,
            team_carousel=data.team_carousel  # Inclui os carrosséis atualizados
        )

@router.put("/{nav_main_content_id}/{carousel_id}")
async def update_carousel(
    carousel_item: TeamCarouselSchema,
    nav_main_content_id: int = Path(..., description="ID do conteúdo principal de navegação"),
    carousel_id: int = Path(..., description="ID específico do carrossel a ser atualizado"),
    session: AsyncSession = Depends(get_session)
):
    # Primeiro, buscamos o conteúdo principal de navegação pelo ID
    nav_main_content_query = select(NavMainContentModel).filter(NavMainContentModel.id == nav_main_content_id)
    nav_main_content_result = await session.execute(nav_main_content_query)
    nav_main_content = nav_main_content_result.scalar_one_or_none()
    
    if not nav_main_content:
        raise HTTPException(status_code=404, detail="Conteúdo principal de navegação não encontrado")

    # Depois, buscamos o carrossel pelo ID específico
    carousel_query = select(TeamCarouselModel).filter(TeamCarouselModel.id == carousel_id)
    carousel_result = await session.execute(carousel_query)
    team_carousel = carousel_result.scalar_one_or_none()
    
    if team_carousel:
        # Atualize o carrossel existente com os novos dados
        for key, value in carousel_item.dict(exclude_unset=True).items():
            setattr(team_carousel, key, value)
        team_carousel.nav_main_content_id = nav_main_content.id
        await session.commit()
        return {"detail": "Carrossel atualizado com sucesso"}
    else:
        # Se o carrossel não existir, crie um novo
        new_carousel = TeamCarouselModel(
            titulo=carousel_item.titulo,
            subtitulo=carousel_item.subtitulo,
            nome=carousel_item.nome,
            cargo=carousel_item.cargo,
            descricao=carousel_item.descricao,
            link1=carousel_item.link1,
            link2=carousel_item.link2,
            link3=carousel_item.link3,
            nav_main_content_id=nav_main_content.id
        )
        session.add(new_carousel)
        await session.commit()
        return {"detail": "Novo carrossel criado com sucesso"}
    



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_composite_data(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        # Deletar AddressComponentModel
        address_query = select(AddressComponentModel).filter(AddressComponentModel.id == id)
        address_result = await session.execute(address_query)
        address_component = address_result.scalar_one_or_none()

        if address_component:
            await session.delete(address_component)
            await session.commit()

        # Deletar ContentSectionModel
        content_query = select(ContentSectionModel).filter(ContentSectionModel.id == id)
        content_result = await session.execute(content_query)
        content_section = content_result.scalar_one_or_none()

        if content_section:
            await session.delete(content_section)
            await session.commit()

        # Deletar InfoMainContentModel
        info_query = select(InfoMainContentModel).filter(InfoMainContentModel.id == id)
        info_result = await session.execute(info_query)
        info_main_content = info_result.scalar_one_or_none()

        if info_main_content:
            await session.delete(info_main_content)
            await session.commit()

        # Deletar NavMainContentModel e carrosséis relacionados
        nav_query = select(NavMainContentModel).filter(NavMainContentModel.id == id)
        nav_result = await session.execute(nav_query)
        nav_main_content = nav_result.scalar_one_or_none()

        if nav_main_content:
            # Deletar TeamCarouselModel relacionado
            carousel_query = select(TeamCarouselModel).filter(TeamCarouselModel.nav_main_content_id == nav_main_content.id)
            carousel_result = await session.execute(carousel_query)
            team_carousels = carousel_result.scalars().all()

            for team_carousel in team_carousels:
                await session.delete(team_carousel)

            # Deletar NavMainContentModel
            await session.delete(nav_main_content)
            await session.commit()

        # Deletar VideoContentModel
        video_query = select(VideoContentModel).filter(VideoContentModel.id == id)
        video_result = await session.execute(video_query)
        video_content = video_result.scalar_one_or_none()

        if address_component is None and content_section is None and info_main_content is None and nav_main_content is None and video_content is None:
            raise HTTPException(detail='Nenhum dado encontrado para o ID fornecido', status_code=status.HTTP_404_NOT_FOUND)

        if video_content:
            await session.delete(video_content)
            await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
