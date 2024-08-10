import requests
import json
from keys import keys
from bs4 import BeautifulSoup


class ConvertException(Exception):
    pass


class CryptoConv:
    @staticmethod
    def convert(base: str, quote: str, amount: float):

        if base == quote:
            raise ConvertException('Вы ввели две одинаковые валюты!')

        try:
            base_ticker, quote_ticker = keys[base], keys[quote]

        except BaseException:
            raise ConvertException('Не удалось обработать валюту!')

        if amount < 0:
            raise ConvertException('Не удалось обработать количество!')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]

        return total_base


def get_exchange_rates():
    url = 'https://www.cbr.ru/currency_base/daily/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Парсинг таблицы с курсами валют

    table = soup.find('table', {'class': 'data'})
    rows = table.find_all('tr')

    # Словарь для сохранения курсов валют
    
    exchange_rates = {}

    for row in rows[1:]:
        columns = row.find_all('td')
        currency = columns[3].text
        rate = columns[4].text
        exchange_rates[currency] = rate

    return exchange_rates
