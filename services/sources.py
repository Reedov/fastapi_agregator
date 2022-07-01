from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.database import get_session
from models.models_orm import Source, SourceType
from schemas import SourceOut, SourceIn, SourceTypeOut, SourseFilters
from typing import List


class SourceService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_by_id(self, source_id: int) -> Source:
        source = (self.session.query(
                                     Source.id,
                                     Source.name.label('name'),
                                     Source.url,
                                     Source.get_items,
                                     Source.is_active,
                                     Source.created_at,
                                     Source.type_id,
                                     Source.get_period_sec,
                                     # SourceType.name.label('type')
                  )
                  # .join(SourceType, Source.type_id == SourceType.id, isouter=True)
                  .filter_by(id=source_id).one())
        if not source:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return source

    def create(self, source_indata) -> SourceOut:
        """ создание новой записи """
        source = Source(**source_indata.dict())
        self.session.add(source)
        self.session.commit()
        return source

    def get_by_id(self, source_id: int) -> SourceOut:
        """ выборка по id """
        return self._get_by_id(source_id)

    def get_all(self, filters: dict = None) -> List[SourceOut]:
        """ выборка всех или по фильтрам """
        query = self.session.query(Source.id,
                                   Source.name.label('name'),
                                   Source.url,
                                   Source.get_items,
                                   Source.is_active,
                                   Source.created_at,
                                   Source.type_id,
                                   Source.get_period_sec,
                                   SourceType.name.label('type'))
        sourse_filters = SourseFilters(**filters)
        if filters:
            query = query.filter_by(**sourse_filters.
                                    dict(exclude_unset=True))  # исключить те которые None
        query = query.join(SourceType, Source.type_id == SourceType.id, isouter=True)
        return query.all()

    def update(self, source_id: int, source_data: SourceIn):
        """ обновление замиси """
        source_data = {key: value for key, value in dict(source_data).items() if value is not None}
        self.session.query(Source).filter(Source.id == source_id).update(values=source_data)
        self.session.commit()
        return self._get_by_id(source_id)

    def delete(self, source_id: int) -> SourceOut:
        source = self._get_by_id(source_id)
        self.session.delete(source)
        self.session.commit()
        return source


class SourceTypeService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, source_type_indata) -> SourceTypeOut:
        """ создание новой записи """
        source_type = SourceType(**source_type_indata.dict())
        self.session.add(source_type)
        self.session.commit()
        return source_type

    def get_all(self) -> List[SourceTypeOut]:
        """ выборка всех или по фильтрам """
        query = self.session.query(SourceType)
        return query.all()
