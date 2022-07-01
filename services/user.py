from fastapi import Depends, HTTPException, status
from models.database import get_session
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.models_orm import User, Source, Subscribes, SourceType, Post
from schemas import UserOut, SourceOut, SubscribesOut, PostOut
from typing import List


class UserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_by_id(self, user_id: int) -> UserOut:
        user = (self.session.query(User)
                .join(Subscribes, User.id == Subscribes.user_id)

                .filter(User.id == user_id)
                # .filter(Source.users == user_id)
                .first())
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    def get_by_id(self, user_id: int) -> UserOut:
        return self._get_by_id(user_id)

    def get_subscribes_id(self, user_id: int) -> list:
        query = (self.session.query(Subscribes.source_id)
                 .filter(Subscribes.user_id == user_id))
        return query.all()

    def get_user_subscribes(self, user_id: int) -> SubscribesOut:
        """ получение подписок пользователя """
        query = (self.session.query(
                                    Subscribes.user_id.label('user_id'),
                                    Source.id,
                                    Source.name,
                                    Source.url,
                                    Source.get_items,
                                    Source.is_active,
                                    Source.type_id,
                                    Source.created_at,
                                    SourceType.name.label('type')
                                    )
                 .join(Source, Source.id == Subscribes.source_id)
                 .join(SourceType, SourceType.id == Source.type_id, isouter=True)
                 .filter(Subscribes.user_id == user_id))
        subscribes = query.all()
        return SubscribesOut(user_id=user_id,
                             sources=[SourceOut(**x) for x in subscribes]
                             )

    def update_user_subscribes(self, user_id, subscribes_in: List[int]) -> SubscribesOut:
        """ обновление подписок пользователя """
        user_subscribes = self.get_subscribes_id(user_id=user_id)  # получаем подписки пользователя
        user_subscribes = set([x[0] for x in user_subscribes] if user_subscribes else [])  # переводим в set
        subscribes_in = set(subscribes_in)
        for_del = user_subscribes - subscribes_in  # разница сетов
        for_add = [Subscribes(user_id=user_id, source_id=x) for x in (subscribes_in - user_subscribes)]
        self.session.bulk_save_objects(for_add)  # пачкой вставляем
        delete_query = (self.session.query(Subscribes).
                        filter(and_(Subscribes.user_id == user_id,
                                    Subscribes.source_id.in_(for_del))
                               )
                        )  # удаляем по user_id  и сету for_del
        delete_query.delete()
        self.session.commit()
        return self.get_user_subscribes(user_id)

    def get_user_posts(self, user_id) -> List[PostOut]:
        query = (self.session.query(Post)
                 .join(Source, Post.source_id == Source.id)
                 .join(Subscribes, Source.id == Subscribes.source_id)
                 .filter(Subscribes.user_id == user_id)
                 )
        return query.all()
