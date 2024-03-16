from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Смайлики "), KeyboardButton(text="Ссылки")],
        [KeyboardButton(text="Калькулятор"), KeyboardButton(text="Спец. кнопки")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True,
)


links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube", url="https://youtube.com/@fsoky"),
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=benzmaxing"),
        ]
    ]
)


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="◀", callback_data=Pagination(action="prev", page=page).pack()
        ),
        InlineKeyboardButton(
            text="▶", callback_data=Pagination(action="next", page=page).pack()
        ),
        width=2,
    )
    return builder.as_markup()
