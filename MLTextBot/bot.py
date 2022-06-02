import asyncio
import logging

from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher

from config import API_TOKEN, admin
from OCR import OCR

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(API_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Добро пожаловать в бота *OCR* (optical character recognition) - оптическое "
                         "распознавание "
                         "символов.\nПросто отправьте фото, а бот в ответ пришлёт обнаруженный на фото текст. \n\nБот "
                         "может долго не отвечать, так как оптическое распознавание символов дело не простое)")


@dp.message_handler(content_types=["photo"])
async def photo(message: types.Message):
    if message.media_group_id:
        return await message.answer("Можно отправлять только одно фото")
    await message.answer("Поиск символов на фото...\nПоиск может занять несколько минут")

    if message.chat.id != admin:
        await bot.send_message(chat_id=admin, text=f"Пользователь *{message.from_user.username}* прислал фото:")
        await bot.copy_message(chat_id=admin, message_id=message.message_id, from_chat_id=message.chat.id)

    destination_file = f"photo/{message.from_user.username}/{message.photo[-1].file_id}.jpg"
    await message.photo[-1].download(destination_file=destination_file)
    text = await text_recognition(destination_file)
    if text == "":
        text = "*Символы на фото не обнаружены(*"
    result = f"*Результат:*\n{text}"
    print(result)
    try:
        await message.reply(result)
    except:
        await message.reply("*Произошла какая-то ошибка(*")
    if message.chat.id != admin:
        await bot.send_message(chat_id=admin, text=f"*{message.from_user.username}*\n{result}")


@dp.message_handler()
async def another_text(message: types.Message):
    await message.answer("Просто отправьте фото")


if __name__ == "__main__":
    executor.start_polling(dp, loop=loop)
