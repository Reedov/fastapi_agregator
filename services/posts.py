from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models_orm import Post, Source, Subscribes
from models.database import get_session
from schemas import PostOut, PostIn, PostFilters


class PostService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, post_indata) -> PostOut:
        """ создание нового поста """
        post = Post(**post_indata.dict())
        self.session.add(post)
        self.session.commit()
        return post

    def _get_by_id(self, post_id: int) -> PostOut:
        """ получение по id """
        post = self.session.query(Post).filter_by(id=post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post

    def get_by_id(self, post_id: int) -> PostOut:
        """ выборка по id """
        return self._get_by_id(post_id)

    def get_all(self, filters: dict) -> List[PostOut]:
        """ выборка всех или по фильтрам """
        query = (self.session.query(Post.id,
                                    Post.title,
                                    Post.posted_at,
                                    Post.url,
                                    Post.content,
                                    Post.img_url,
                                    Source.name.label('source_name')))

        if filters:
            post_filters = PostFilters(**filters)
            query = query.filter_by(**post_filters.dict(exclude_unset=True))  # исключить те которые None

        query = (query
                 .join(Subscribes, Post.source_id == Subscribes.source_id)
                 .join(Source, Subscribes.source_id == Source.id)
                 .filter(Subscribes.user_id == filters.pop('user_id'))
                 .order_by(Post.posted_at.desc()))

        return query.all()

    def update(self, post_id: int, post_data: PostIn):
        """ обновление замиси """
        post = self._get_by_id(post_id)
        for key, value in post_data:
            setattr(post, key, value)
        self.session.commit()
        return post

    def delete(self, post_id: int) -> PostOut:
        post = self._get_by_id(post_id)
        self.session.delete(post)
        self.session.commit()
        return post
