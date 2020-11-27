import requests
from pprint import pprint
import time
from datetime import datetime

def convertingDateUNIX(date):
    return datetime.utcfromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")


# Стандартное количество вопросов из запроса
number_questions_request = 30
# Определим сегодняшнюю дату
now = datetime.now()
# дата в формате UNIX
now_unix = time.mktime(now.timetuple())
# переменная, в которую записываем последнюю дату, которая была в запросе. Изначально - 2 дня ранее
let_unix = now_unix - 2 * 86400
# лист с датами создания вопросов
date_list = []
# будем вызывать запрос вызывать запрос, пока верно условие (в последней итерации колиество запросов будет в диапозоне 0 < x < 30)
while number_questions_request == 30:
    # в параметры min и max запишем переменную и текщую дату
    params = {
        'order': 'asc',
        'min': str(int(let_unix)),
        'max': str(int(now_unix)),
        'sort': 'creation',
        'tagged': 'python',
        'site': 'stackoverflow'
    }
    resp = requests.get(
        'https://api.stackexchange.com/2.2/questions?', params=params)
    if resp.status_code != 200:
      raise Exception(f"Ошибка {resp.status_code}")

    data = resp.json()['items']
    # перезапишем количество вопросов, полученое из запроса
    number_questions_request = len(data)
    for elem in data:
        # переопределим переменную, записав в нее дату последнего вопроса
        let_unix = int(elem['creation_date'])
        # выведем вопросы
        print(f'Вопрос:  {elem["title"]}')
        print(f'Дата:  {convertingDateUNIX(let_unix)}')
        print(f'Теги: {elem["tags"]}')
        print()
        # запишем дату в date_list
        date_list.append(convertingDateUNIX(let_unix))
# для проверки выведем даты создания первого и последнего вопросов
print(date_list[0], date_list[-1])