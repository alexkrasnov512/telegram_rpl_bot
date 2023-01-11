from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hide_link
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tokens import API_TOKEN
from project_for_me import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

HELP_COMMAND = """
<b> /help </b> - <em> Список команд </em>
<b> /start </b> - <em> Старт бота </em>
<b> /description </b> - <em> Описание бота </em>
"""


ikb = InlineKeyboardMarkup(row_width=2)
but_1 = InlineKeyboardButton(text='Вывести следующие 3 новости?', callback_data='next')
but_2 = InlineKeyboardButton(text='Ввести другую команду', callback_data='another')
ikb.add(but_1).add(but_2)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет, я rpl_news_bot!")
    await message.delete()


@dp.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer("Я помогаю узнать самые свежие новости о твоей любимой российской"
                         " команде! От тебя требуется только ввести ее название!)")
    await message.delete()


count = 0
team1 = ''


@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    global team1
    global count
    count = 0
    team1 = message.text
    my_news = pretty_news_message(message.text, count)
    if type(my_news) is dict:
        for k, v in my_news.items():
            await message.answer('<b>' + k + '</b>' + '\n' + '\n' + v[0] + '\n' + f"{hide_link(v[1])}",
                                 parse_mode="HTML")
        await message.answer(text='Хотите еще новости?', reply_markup=ikb)
    else:
        await message.answer(my_news)


@dp.callback_query_handler(text="next")
async def next_news(callback: types.CallbackQuery) -> None:
    global team1
    global count
    count += 3
    my_news2 = pretty_news_message(team1, count)
    if type(my_news2) is str:
        await callback.message.answer(text='Свежих новостей больше нет, введите другую команду!')
    else:
        for k, v in my_news2.items():
            await callback.message.answer('<b>' + k + '</b>' + '\n' + '\n' + v[0] + '\n' + f"{hide_link(v[1])}",
                                          parse_mode="HTML")
        await callback.message.answer(text='Хотите еще новости?', reply_markup=ikb)


@dp.callback_query_handler(text="another")
async def next_news(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(text='Введите другую команду')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
