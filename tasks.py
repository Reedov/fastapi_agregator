import asyncio
import datetime

from news_parser import rss_parse
from models.models_orm import Source, Post, SourceGet
from schemas import PostIn, SourceGetIn
from typing import List
from models.database import Session
from sqlalchemy.dialects.sqlite import insert

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s [%(funcName)s:%(lineno)s] %(message)s',)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_sources() -> list:
    """ получение активных ресурсов """
    with Session() as session:
        sources = (session.query(Source.id,
                                 Source.get_period_sec,
                                 Source.url,
                                 Source.get_items,
                                 SourceGet.get_at
                                 )
                   .join(SourceGet, Source.id == SourceGet.source_id)
                   .filter(Source.is_active == True)
                   .all())
        # если timedelta ресурса больше чем get_period_sec
        sources = [x for x in sources if x.get_period_sec <= (datetime.datetime.now() - x.get_at).seconds]
        return sources


async def get_posts():
    sources = get_sources()
    rss_data: List[PostIn] = []
    if sources:
        rss_data = [y for x in await rss_parse.get_rss_scope(sources) if x for y in x]
        with Session() as session:

            # вставка постов
            insert_req = insert(Post).values([{**x.dict()} for x in rss_data])
            insert_req = insert_req.on_conflict_do_nothing(
                index_elements=('source_id', 'title'),
            )
            session.execute(insert_req)

            # обновление времени получения
            update_data = [SourceGetIn(source_id=x.id, get_at=datetime.datetime.now()) for x in sources]
            update_req = insert(SourceGet).values([{**x.dict()} for x in update_data])
            update_req = update_req.on_conflict_do_update(
                index_elements=('source_id',),
                set_=dict(get_at=update_req.excluded.get_at)  # что нужно обновить
            )
            session.execute(update_req)

            session.commit()
    logger.info(f'sources: {len(sources)} news: {len(rss_data)}')

if __name__ == "__main__":
    from time import sleep
    logger.info('start')
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_posts())
        sleep(60)

# RABBIT_LOGING = 'rabbitmq'
# RABBIT_PASS = 'rabbitmq'
# RABBIT_URL = '127.0.0.1'
# broker = f'amqp://{RABBIT_LOGING}:{RABBIT_PASS}@{RABBIT_URL}//'
#
# app = Celery('some_tasks',
#              broker=broker,  # брокер для хранения очередей задач
#              backend='db+sqlite:///db.sqlite3'  # база для хранения результата, для работы нужна sqlalchemy
#              )
#
#
# @app.task
# def reverse(text):
#     sleep(5)
#     return text[::-1]
