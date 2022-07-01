""" тесты для парсера """
from datetime import datetime
import pytest
import re
from news_parser import utils


@pytest.mark.parametrize('datetime_from_text',
                         ["2020-01-01 01:30", "02:35", "Вчера 12:20", " 14:20 СЕГОДНЯ", "2022-10-01"])
def test_time_converter(datetime_from_text):
    _date_time = utils.time_converter(datetime_from_text)
    assert re.match(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d',
                    datetime.strftime(_date_time, "%Y-%m-%d %H:%M"))

