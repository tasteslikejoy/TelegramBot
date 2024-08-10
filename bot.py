import telebot
from config import TOKEN
from extensions import ConvertException, CryptoConv, get_exchange_rates
from keys import keys


bot = telebot.TeleBot(TOKEN)

#  Команда start запускает приветственное сообщение


@bot.message_handler(commands=['start'])
def get_start(message: telebot.types.Message):
    text = (
        'Что бы начать работу введите: <Имя валюты> <Имя покупаемой валюты> <Количество> '
        '\nУвидеть список всех валют: /values'
        '\nУвидеть список валюты относительно 1 Рубля: /rate')
    bot.reply_to(message, text)

#  Команда values выводит список доступной валюты


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#  Команда rate выводит списоб валюты относительно 1 рубля


@bot.message_handler(commands=['rate'])
def rates(message):
    exchange_rates = get_exchange_rates()
    response = 'Курсы валют:\n\n'

    for currency, rate in sorted(
            exchange_rates.items(), key=lambda x: str(x[1])):
        response += f'{currency}: {rate}\n'

    bot.reply_to(message, response)

#  Обработка текста


@bot.message_handler(content_types=['text'])
def get_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Не верное количество параметров!')

        base, quote, amount = values

        amount = float(amount)

        total_base = CryptoConv.convert(base, quote, amount)

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка со стороны пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {base} в {quote} - {total_base * amount}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
