from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (Column, Integer, String, Boolean,
                        ForeignKey, DateTime, TIMESTAMP,
                        func, Table, UniqueConstraint, Constraint)

Base = declarative_base()

user_sources = Table('user_sources', Base.metadata,
                     Column('user_id', ForeignKey('users.id'), primary_key=True),
                     Column('source_id', ForeignKey('sources.id'), primary_key=True)
                     )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    birthdate = Column(DateTime)
    second_name = Column(String)
    first_name = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=func.now())
    # updated_at = Column(TIMESTAMP, nullable=False,
    #                     server_default=func.now(),
    #                     onupdate=func.now())
    # __table_args__ = (UniqueConstraint('username', 'email', name='username_constr'))


class Subscribes(Base):
    __tablename__ = 'subscribes'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    source_id = Column(String)
    # __table_args__ = (UniqueConstraint('user_id', 'source_id', name='user_source_constr'),)


class SourceType(Base):
    __tablename__ = 'source_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    get_items = Column(Integer)
    is_active = Column(Boolean)
    type_id = Column(Integer,
                     # ForeignKey('source_type.id')
                     )
    get_period_sec = Column(Integer)
    icon = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())
    # users = relationship("User", secondary="user_sources",
    #                      # back_populates='sources'.
    #                      )


class SourceGet(Base):
    __tablename__ = 'sources_get'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    get_at = Column(TIMESTAMP)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    posted_at = Column(DateTime)
    source_id = Column(Integer,
                       # ForeignKey('sources.id')
                       )
    title = Column(String)
    content = Column(String)
    url = Column(String)
    img_url = Column(String)
    created_at = Column(TIMESTAMP, default=func.now())


# class Icon(Base):
#     __tablename__ = 'icon'
#     id = Column(Integer, primary_key=True)
#     img = Column(String, unique=True, nullable=False)
#     name = Column(String, nullable=False)
#     mimetype = Column(String, nullable=False)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    engine = create_engine("sqlite:///database.db")
    session = Session(binds=engine)
    query = session.query(Source).all()
