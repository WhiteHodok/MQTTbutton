import asyncio
import logging
import sys
import platform
from aiogram.methods import DeleteWebhook
from config import dp, bot
from src.handlers.user_handler import user_router
from src.func import MQTTListener, mqtt_listener, set_mqtt_listener

# Фикс для Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start():
    # 1. Создаем MQTTListener
    mqtt_listener_instance = MQTTListener(bot=bot)

    # 2. Устанавливаем глобальный экземпляр
    set_mqtt_listener(mqtt_listener_instance)

    # 3. Запускаем MQTT клиент
    await mqtt_listener_instance.start()
    logging.info("MQTT listener initialized")

    # 4. Подключаем роутеры
    dp.include_routers(user_router)

    # 5. Запускаем бота
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        await mqtt_listener_instance.stop()
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    asyncio.run(start())