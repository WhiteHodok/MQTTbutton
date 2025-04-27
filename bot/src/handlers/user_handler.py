from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import bot
from src.func import get_mqtt_listener  # Вместо прямого импорта используем функцию
from src.keyboards.user_keyboard import user_keyboard, cancel_board, user_keyboard_button, user_cancel_button
from src.phrases import START, LISTENING
from src.states.user_states import User
import logging

user_router = Router()
logger = logging.getLogger(__name__)


@user_router.message(CommandStart(), StateFilter(None))
async def start_command(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, START, reply_markup=user_keyboard())
        await state.set_state(User.main)
        logger.info(f"User {chat_id} started the bot")
    except Exception as e:
        logger.error(f"Start command error: {e}")


@user_router.message(F.text == user_keyboard_button['button1'], StateFilter(User.main))
async def start_listening(message: Message, state: FSMContext):
    try:
        mqtt_listener = get_mqtt_listener()  # Получаем актуальный экземпляр
        if not mqtt_listener:
            logger.critical("MQTT listener not initialized!")
            await message.answer("🚫 Сервис временно недоступен")
            return

        mqtt_listener.add_chat(message.chat.id)
        logger.info(f"Added listener for chat {message.chat.id}")

        await message.answer(
            "🔊 Режим реального времени активирован",
            reply_markup=cancel_board()
        )
        await state.set_state(User.listen)

    except Exception as e:
        logger.error(f"Listen start error: {e}")
        await message.answer("⚠️ Произошла ошибка, попробуйте позже")


@user_router.message(F.text == user_cancel_button['cancel'], StateFilter(User.listen))
async def stop_listening(message: Message, state: FSMContext):
    try:
        mqtt_listener = get_mqtt_listener()  # Получаем актуальный экземпляр
        if not mqtt_listener:
            logger.critical("MQTT listener not initialized!")
            return

        mqtt_listener.remove_chat(message.chat.id)
        logger.info(f"Removed listener for chat {message.chat.id}")

        await message.answer(
            "Прослушка остановлена",
            reply_markup=user_keyboard()
        )
        await state.set_state(User.main)

    except Exception as e:
        logger.error(f"Listen stop error: {e}")
        await message.answer("⚠️ Произошла ошибка, попробуйте позже")