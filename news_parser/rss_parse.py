import feedparser
from datetime import datetime, timedelta
import time
import re
from news_parser import fetch_bs
from news_parser.constants import *
from schemas import PostIn, SourceOut
import logging
import asyncio
from typing import List
logging.basicConfig(format='%(asctime)s [%(funcName)s]  %(message)s', level=logging.INFO)  # INFO DEBUG
logger = logging.getLogger(__name__)


def get_post_time(dt: time.struct_time) -> datetime:
    datetime_type = datetime(*dt[:5])  # в формат datetime
    return datetime_type + timedelta(hours=3)  # разница в 3 часа


def find_description(description_soup: fetch_bs) -> str:
    if description_soup and len(description_soup):
        description_text = re.sub(r'\s+', ' ', description_soup.text)
    else:
        description_text = '<;('
    description_text = re.sub(CENSOR, " ", description_text)
    if len(description_text) > 100:
        description_text = ".".join(description_text.split(".")[:2])[:350]  # 2 предложения не больше 350 знаков
    return description_text


def parse_entry(entry):
    """ поиск в rss элементов """
    title = entry.get('title')  # название новости
    link = str(entry.get('link'))  # ссылка на новость
    links = entry.get('links')
    image_dct = [x for x in links if x.get('type') == 'image/jpeg']
    description_soup = fetch_bs.make_soup(entry.get('description'))
    description = find_description(description_soup)
    image = image_dct[0].get('href', '') if image_dct else ''
    if description_soup and not image:
        if imagetag := description_soup.find('img'):
            image = imagetag.get('src', '')
    post_time = get_post_time(entry.updated_parsed)
    return PostIn(posted_at=post_time,
                  title=title,
                  content=description,
                  url=link,
                  img_url=image)


async def get_news(source: SourceOut) -> List[PostIn]:
    """ получает список новостей rss по ссылке
    url: str, source_id: str, feed_count: int
    """
    _lst = []
    raw_data = await fetch_bs.get_page_async(source.url)
    if raw_data:
        rss = feedparser.parse(raw_data.text)
        rss_lst = rss.get('entries')
        for entry in rss_lst[:source.get_items]:  # считываем feed_count  фидов
            parsed_entry = parse_entry(entry)
            parsed_entry.source_id = source.id
            # parsed_entry.source_name = source_name
            _lst.append(parsed_entry)
    return _lst


async def get_rss_scope(rss_sourses: list[SourceOut]):
    tasks = list()
    for sourse in rss_sourses:
        tasks.append(asyncio.create_task(get_news(sourse)))
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    SOURSES = [('http://lenta.ru/rss/news', 1, 3),
               ('http://www.kommersant.ru/RSS/news.xml', 2, 2),
               ('https://sochi-express.ru/feed', 3, 3),
               ('http://www.ixbt.com/export/news.rss', 4, 2),
               ]
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_rss_scope(SOURSES))
