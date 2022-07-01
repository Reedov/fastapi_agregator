import pytest
from news_parser import rss_parse
from ..schemas import PostOut, SourceOut


@pytest.mark.parametrize('source',
                         [('http://lenta.ru/rss/news', 'lenta', 3)])
def test_rss(source):
    news = rss_parse.get_news(source)
    assert type(news) == PostOut

