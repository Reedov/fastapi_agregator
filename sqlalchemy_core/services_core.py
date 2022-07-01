from database.db_connect import connection
from sqlalchemy_core.models_core import sources_table, posts_table
from schemas import SourceIn, PostListIn
from sqlalchemy import select, insert, update, delete, engine
from typing import List


async def get_sources() -> list:
    """ получение всех ресурсов"""
    query = select(
        [sources_table.c.id,
         sources_table.c.name,
         sources_table.c.url,
         sources_table.c.get_items,
         sources_table.c.is_active]
    )
    return connection.execute(query).fetchall()


async def get_source_by_id(source_id: int) -> engine.row.LegacyRow:
    """ получение ресурса по id """
    query = select(
        [sources_table.c.id,
         sources_table.c.name,
         sources_table.c.url,
         sources_table.c.get_items,
         sources_table.c.is_active]
    ).where(sources_table.c.id == source_id)
    return connection.execute(query).fetchone()


async def get_source_by_url(url: str) -> engine.row.LegacyRow:
    """ получение ресурса по id """
    query = select(
        [sources_table.c.id,
         sources_table.c.name,
         sources_table.c.url,
         sources_table.c.get_items,
         sources_table.c.is_active]
    ).where(sources_table.c.url == url)
    return connection.execute(query).fetchone()


async def post_source(source: SourceIn):
    """ вставка нового ресурса """
    query = (sources_table.insert()
             .values(
                    name=source.name,
                    url=source.url,
                    get_items=source.get_items,
                    is_active=source.is_active
                    )
             # not supported by sqllite3:
             # sqlalchemy.exc.CompileError: RETURNING is not supported by this dialect's statement compiler
             # .returning(sources_table.c.id,
             #            sources_table.c.name,
             #            sources_table.c.url,
             #            sources_table.c.get_items,
             #            sources_table.c.is_active)
             )
    connection.execute(query)

    query = select(
        [sources_table.c.id,
         sources_table.c.name,
         sources_table.c.url,
         sources_table.c.get_items,
         sources_table.c.is_active]
    ).where(sources_table.c.url == source.url)

    return connection.execute(query).fetchone()


async def patch_source(source_id: int, sourse: SourceIn):
    """ update(patch) ресурса """
    query = (update(sources_table).
             where(sources_table.c.id == source_id).
             values(**sourse.dict(exclude_unset=True))  # exclude_unset исключает подстановку не переданных полей
             )
    return connection.execute(query)


async def delete_source(source_id: int):
    """ удаление ресурса по id """
    query = delete(sources_table).where(sources_table.c.id == source_id)
    return connection.execute(query)

"""
source_name='komersant'
post_list=[PostIn(post_time=datetime.datetime(2022, 6, 12, 14, 39),
                  title='«Транснефть» сообщила о ',
                  content=None,
                  url=None,
                  img_url=None),
            PostIn(post_time=datetime.datetime(2022, 6, 12, 14, 3),
                   title='Шри-Ланка допустила возвращение к импорту российской нефти'
"""


async def insert_posts(posts_data_list: List[PostListIn]) -> int:
    """ вставка постов с ресурса """
    for item in posts_data_list:
        source_id = (connection.execute(select(sources_table.c.id).where(sources_table.c.name == item.source_name))
                     .fetchone()
                     )
        data = {**item.dict(), 'source_id': source_id}
        query = insert(posts_table)
        connection.execute(query, data)
    return len(posts_data_list)


async def get_posts():
    """ получение постов """
    j = posts_table.join(sources_table, posts_table.c.source_id == sources_table.c.id)
    query = select(
        [posts_table.c.id,
         posts_table.c.posted_at,
         posts_table.c.source_id,
         posts_table.c.title,
         posts_table.c.content,
         posts_table.c.url,
         posts_table.c.img_url]
    ).select_from(j)
    return connection.execute(query).fetchall()

