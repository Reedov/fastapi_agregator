from datetime import datetime, timedelta
import re
from constants import TODAY, YESTERDAY


def time_converter(_time):
    """
    конвертирует время типа сегодя, 22:30 в 2022-04-28 22:30
    если только дата(формат YYYY-MM-DD) - добавляется текущее время
    если только время(формат HH:MM) - добавляется текущая дата
    """
    now = datetime.now()
    if cleared_time := re.search(r"\d{1,2}:\d{1,2}", _time):  # поиск времени
        cleared_time = cleared_time.group(0)
    else:
        cleared_time = now.time().strftime('%H:%M')
    if cleared_date := re.search(r"\d\d\d\d-\d\d-\d\d", _time):  # поиск времени
        cleared_date = cleared_date.group(0)
    else:
        cleared_date = now.time().strftime('"%Y-%m-%d')

    # если 'сегодня' или обозначено только время.
    if (re.search(r"^\d{1,2}:\d{1,2}$", _time.strip())
            or any(x in _time.lower() for x in TODAY)):
        today_date = f'{now.year:04d}-{now.month:02d}-{now.day:02d}'
        _time = f'{today_date} {cleared_time}'
    # если вчера
    elif any(x in _time.lower() for x in YESTERDAY):
        yesterday = now - timedelta(days=1)
        yesterday_date = f'{yesterday.year:04d}-{yesterday.month:02d}-{yesterday.day:02d}'
        _time = f'{yesterday_date} {cleared_time}'
    else:
        _time = f'{cleared_date} {cleared_time}'

    return datetime.strptime(_time, "%Y-%m-%d %H:%M")


def get_time_now():
    now = datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}"


def valid_order(_date: str) -> str:
    """если 01.02.1900 или 1900.02.01
    returns(str) like '1900-02-01' """
    time_lst = _date.split('.')
    if len(time_lst[2]) > 2:
        valid_order_date = [re.sub(r'\D', '', x) for x in time_lst[::-1]]
    else:
        valid_order_date = [re.sub(r'\D', '', x) for x in time_lst]
    valid_order_date = '-'.join(valid_order_date)
    return valid_order_date


if __name__ == '__main__':
    t = time_converter('2021-01-01')  # '00:07'
    print(t)
    print(type(t))
