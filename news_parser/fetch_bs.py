"""connect to site, return soup."""
# import requests
import httpx
from bs4 import BeautifulSoup
import logging

import asyncio

logging.basicConfig(format='%(asctime)s - %(module)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger("fetch_bs")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
user_agent_mobile = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)' \
                    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36'  # андроид

headers = {
           'User-Agent': user_agent,
           'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
          }
TIMEOUT = 5.0


async def get_page_async(url, **params) -> httpx.Response:
    """make get request"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=TIMEOUT, follow_redirects=True)
            return response
    except httpx.ConnectError:
        logger.error(f'{url} ConnectError')
    except Exception as e:
        logger.error(f'{url} {e}')


# def get_page_sync(url) -> requests.Response:
#     """return requests.get object"""
#     try:
#         answer = requests.get(url, headers=headers, timeout=4)
#         if answer.status_code == 200:
#             return answer
#     except Exception as e:
#         logger.error(e)


def make_soup(page: str) -> BeautifulSoup:
    """ return BeautifulSoup class from html """
    if page:
        return BeautifulSoup(page, 'html.parser')


async def main(url):
    page = await get_page_async(url)
    if not page:
        return
    soup = make_soup(page.text)
    print(type(soup))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('http://lenta.ru/rss/news'))
