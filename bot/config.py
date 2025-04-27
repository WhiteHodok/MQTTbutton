import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings



class EnvSettings(BaseSettings):
    """
    Environment settings.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class BotSettings(EnvSettings):
    token: str


class MQTTsetting:
    MQTT_SERVER = ""  # Прямое указание IP
    MQTT_USER = "root" # имя от москита
    MQTT_PASS = "" # пароль от москита
    MQTT_TOPIC = "esp32/button" # название топика

    # Для диагностики
    @classmethod
    def show_config(cls):
        print(f"\nMQTT Config:"
              f"\nServer: {cls.MQTT_SERVER}"
              f"\nUser: {cls.MQTT_USER}"
              f"\nTopic: {cls.MQTT_TOPIC}\n")


bot_settings = BotSettings()

default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=bot_settings.token, default=default)
dp = Dispatcher()

