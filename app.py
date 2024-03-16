import asyncio
from contextlib import suppress

from aiogram import Dispatcher, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from kb import *

bot = Bot("6392263275:AAHYtfXJjoZZELMLYrn5mWW48f5RnmN5mTY", parse_mode="HTML")
dp = Dispatcher()


# photo_id | name | age | location | some about me
anketa = [
    [
        "AgACAgQAAxkBAAMrZfYFQ7QpqSSMVPR_9OPQsn91ONgAAkO9MRvOhbFTDVqpM4xldmgBAAMCAANzAAM0BA",
        "Алиса",
        "20",
        "Москва",
        "Люблю рисовать и тебя <3",
    ],
    [
        "AgACAgQAAxkBAAMsZfYFz34pIIL5X8BRgX-192qUmsAAAkS9MRvOhbFT4QZfxU9fMbQBAAMCAANzAAM0BA",
        "organic",
        "25",
        "Нижний Новгород",
        "пошел нахуй",
    ],
    [
        "gACAgQAAxkBAAMtZfYGVNztLCFLvEykAwRAMtY8XfwAAka9MRvOhbFT0YydpbM2txcBAAMCAANzAAM0BA",
        "Lovv girl <3 :3",
        "34",
        "Ростов-на-Дону",
        "хз че тут написать sorry",
    ],
]


@dp.message(Command("start"))
async def process_start_command(message: Message):
    await message.answer(f"Првиет {message.from_user.first_name}", reply_markup=main_kb)


@dp.callback_query(Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(anketa) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{anketa[page][0]} <b>{anketa[page][2]}</b>", reply_markup=paginator(page)
        )
    await call.answer("")


@dp.message(F.photo)
async def scan_message(message: Message):
    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f"file_id: {file_info.file_id}")
    print(f"file_path: {file_info.file_path}")
    print(f"file_size: {file_info.file_size}")
    print(f"file_unique_id: {file_info.file_unique_id}")


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "ссылки":
        await message.answer("Вот ваши ссылки: ", reply_markup=links_kb)
    elif msg == "спец. кнопки":
        await message.answer("мне лень")
    elif msg == "смайлики":
        await message.answer(
            f"{anketa[0][0]} <b>{anketa[0][1]}</b>", reply_markup=paginator()
        )
    elif msg == "чота":
        await message.answer_photo(
            anketa[0][0], caption=f"{anketa[0][1]}\n{anketa[0][2]}"
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
