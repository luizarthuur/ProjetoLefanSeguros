from fastapi import APIRouter

from api.v1.endpoints import Texto
from api.v1.endpoints import Imagens


api_router = APIRouter()
api_router.include_router(Texto.router, prefix='/Texto', tags=['Texto'])

#api_router.include_router(Imagens.router, prefix='/Imagens', tags=['Imagens'])