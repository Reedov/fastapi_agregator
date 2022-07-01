from fastapi import APIRouter, HTTPException
from schemas import SourceOut, SourceIn, PostOut
from sqlalchemy_core import services_core
from typing import List

router = APIRouter()


@router.get('/')
async def mainapp(response_model=dict):
    return {'response': 'is ok'}


@router.get('/sources', response_model=List[SourceOut])
async def get_sources():
    """ получает список ресурсов """
    return await services_core.get_sources()


@router.get('/sources/{source_id}', response_model=SourceOut)
async def get_source_by_id(source_id: int):
    """ получает ресурсов по id"""
    return await services_core.get_source_by_id(source_id=source_id)


@router.post('/sources', response_model=SourceOut)
async def post_sources(source: SourceIn):
    """ вставляет новый ресурс """
    if await services_core.get_source_by_url(source.url):
        raise HTTPException(status_code=409, detail=f" '{source.url}' already exists")
    return await services_core.post_source(source)


@router.patch('/sources/{source_id}', response_model=SourceOut)
async def patch_source(source_id: int, source: SourceIn):
    """ обновляет ресурс """
    if not await services_core.get_source_by_id(source_id):
        raise HTTPException(status_code=404, detail=f" id:{source_id} not exists")
    await services_core.patch_source(source_id, source)
    return await services_core.get_source_by_id(source_id=source_id)


@router.delete('/sources/{source_id}', response_model=SourceOut)
async def delete_source_by_id(source_id: int):
    if deleted_source := await services_core.get_source_by_id(source_id=source_id):
        await services_core.delete_source(source_id)
    else:
        raise HTTPException(status_code=404, detail=f" '{deleted_source} not exists")

    if not await services_core.get_source_by_id(source_id=source_id):
        raise HTTPException(status_code=500, detail=f" '{source_id} not deleted")
    return deleted_source


@router.get('/posts', response_model=List[PostOut])
async def get_posts():
    """ получает список ресурсов """
    return await services_core.get_posts()
