import asyncio
import json
import logging
from aiomqtt import Client as MqttClient
from aiogram import Bot
from config import MQTTsetting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MQTT")


class MQTTListener:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.active_chats = set()
        self.client = None
        self._task = None

    async def start(self):
        """Запуск MQTT клиента"""
        self._task = asyncio.create_task(self._mqtt_loop())
        logger.info("MQTT listener task started")

    async def _mqtt_loop(self):
        """Основной цикл обработки сообщений"""
        while True:
            try:
                async with MqttClient(
                        hostname=MQTTsetting.MQTT_SERVER,
                        port=1883,
                        username=MQTTsetting.MQTT_USER,
                        password=MQTTsetting.MQTT_PASS
                ) as client:
                    self.client = client
                    await client.subscribe(MQTTsetting.MQTT_TOPIC)
                    logger.info("Подключено к MQTT брокеру")

                    async for message in client.messages:
                        await self._process_message(message)

            except Exception as e:
                logger.error(f"Ошибка подключения: {e}")
                await asyncio.sleep(5)

    async def _process_message(self, message):
        """Обработка входящих сообщений"""
        try:
            payload = json.loads(message.payload.decode())
            logger.info(f"Получено: {payload}")

            # Форматирование сообщения
            text = self._format_message(payload)

            # Проверка активных чатов
            logger.info(f"Активные чаты: {self.active_chats}")

            # Отправка всем активным чатам
            if not self.active_chats:
                logger.info("Нет активных чатов для отправки")
                return

            for chat_id in list(self.active_chats):
                try:
                    logger.info(f"Попытка отправки в чат {chat_id}: {text}")
                    await self.bot.send_message(chat_id, text)
                    logger.info(f"Успешно отправлено в чат {chat_id}")
                except Exception as e:
                    logger.error(f"Ошибка отправки в чат {chat_id}: {e}")
                    # Возможно, чат больше не доступен или пользователь заблокировал бота
                    self.active_chats.discard(chat_id)

        except json.JSONDecodeError:
            logger.error(f"Невалидный JSON: {message.payload}")
        except Exception as e:
            logger.error(f"Ошибка обработки: {e}")

    def _format_message(self, payload: dict) -> str:
        """Форматирование сообщения для отправки"""
        event = payload.get("event", "unknown")
        count = payload.get("count", 1)

        # Форматирование сообщения с учетом типа события и счетчика
        if event == "press":
            return f"🔘 Нажатие кнопки (счетчик: {count})"
        elif event == "long_press":
            return f"🔴 Долгое нажатие кнопки (счетчик: {count})"
        elif event == "series_end":
            return f"🔢 Серия завершена: {count} нажатий"
        else:
            return f"❓ Неизвестное событие: {event} (счетчик: {count})"

    def add_chat(self, chat_id: int):
        self.active_chats.add(chat_id)
        logger.info(f"Добавлен чат {chat_id}. Активные чаты: {self.active_chats}")

    def remove_chat(self, chat_id: int):
        self.active_chats.discard(chat_id)
        logger.info(f"Удален чат {chat_id}. Активные чаты: {self.active_chats}")

    async def stop(self):
        """Остановка MQTT клиента"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self.client:
            await self.client.disconnect()
        logger.info("MQTT listener stopped")


# Глобальный экземпляр
mqtt_listener = None

# Функция для установки глобального экземпляра
def set_mqtt_listener(listener_instance):
    global mqtt_listener
    mqtt_listener = listener_instance
    logger.info("Global MQTT listener instance has been set")

# Функция для безопасного получения экземпляра
def get_mqtt_listener():
    global mqtt_listener
    return mqtt_listener