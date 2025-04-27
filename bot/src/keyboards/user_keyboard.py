from aiogram.types import InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import hashlib

user_keyboard_button = {"button1": "🎧Прослушка кнопки", "button2": "📞Зачем этот бот нужен?"}


def user_keyboard():
    """
    Creates a user keyboard with two buttons.

    Returns:
        ReplyKeyboardMarkup: The user keyboard with two buttons.
    """
    user_keyboard = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=user_keyboard_button['button1'])

    button2 = KeyboardButton(text=user_keyboard_button['button2'])

    user_keyboard.row(button1)
    user_keyboard.row(button2)

    return user_keyboard.as_markup(resize_keyboard=True)

user_cancel_button = {"cancel": "❌Отмена"}

def cancel_board():
    cancel_board = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=user_cancel_button['cancel'])
    cancel_board.row(button1)

    return cancel_board.as_markup(resize_keyboard=True)
