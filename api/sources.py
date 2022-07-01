from fastapi import APIRouter, Depends
from typing import List
from schemas import SourcePatchOut, SourceIn, SourceOut, SourceTypeIn, SourceTypeOut
from services.sources import SourceService, SourceTypeService

router = APIRouter(prefix='/sources')


@router.get('/{source_id}', response_model=SourceOut)
def get_source_by_id(source_id: int,
                     service: SourceService = Depends()
                     ):
    """ получение ресурса по id"""
    return service.get_by_id(source_id=source_id)


@router.get('/', response_model=List[SourceOut])
def get_sources(is_active: bool = None,
                get_items: int = None,
                service: SourceService = Depends()
                ):
    """ Получение ресурсов """
    filters = {}
    if is_active is not None:
        filters.update({'is_active': is_active})
    if get_items is not None:
        filters.update({'get_items': get_items})
    return service.get_all(filters=filters)


@router.post('/', response_model=SourceOut)
def post_source(source_indata: SourceIn,
                service: SourceService = Depends()
                ):
    """ создание ресурса """
    return service.create(source_indata=source_indata)


@router.patch('/{source_id}', response_model=SourcePatchOut)
def patch_source(source_id: int,
                 source_indata: SourceIn,
                 service: SourceService = Depends()
                 ):
    """ обновление ресурса """
    source = service.update(source_id, source_indata)
    return source


@router.delete('/{source_id}', response_model=SourceOut)
def delete_source(source_id: int,
                  service: SourceService = Depends()
                  ):
    """ удаление ресурса"""
    return service.delete(source_id=source_id)


@router.post('/sourse_type/', response_model=SourceTypeOut)
def post_source_type(source_type_data: SourceTypeIn,
                     service: SourceTypeService = Depends()
                     ):
    """ создание типа ресурса """
    return service.create(source_type_indata=source_type_data)


@router.get('/sourse_type/', response_model=List[SourceTypeOut])
def get_sources(
                service: SourceTypeService = Depends()
                ):
    """ Получение всех типов ресурса """
    return service.get_all()
