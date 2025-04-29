# MQTT Button Controller with Telegram Bot Integration

[![GitHub stars](https://img.shields.io/github/stars/WhiteHodok/MQTTbutton?style=for-the-badge)](https://github.com/WhiteHodok/MQTTbutton)
[![ESP32](https://img.shields.io/badge/ESP32-S3-00979D?style=for-the-badge&logo=espressif)](https://www.espressif.com/)
[![MQTT](https://img.shields.io/badge/MQTT-3.1.1-660066?style=for-the-badge&logo=eclipsemosquitto)](https://mosquitto.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://python.org)

Управление физической кнопкой через MQTT с интеграцией Telegram бота. Проект позволяет отслеживать различные типы нажатий кнопки и взаимодействовать с устройством через Telegram.

## 🔥 Основные возможности

- 📶 Отслеживание статуса подключения (WiFi/MQTT) на OLED-дисплее
- 🔘 Обнаружение различных типов нажатий:
  - Одиночные нажатия
  - Серии быстрых нажатий
  - Длинные удержания
- 📡 Публикация событий через MQTT брокер
- 🤖 Полноценная интеграция с Telegram:
  - Получение уведомлений в реальном времени
  - Просмотр статистики нажатий
  - Управление через чат
- 📊 Визуализация состояния на OLED-дисплее

## 📦 Установка и настройка

### Для ESP32

1. Установите необходимые библиотеки в Arduino IDE:
   - Adafruit GFX Library
   - Adafruit SSD1306
   - PubSubClient

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/WhiteHodok/MQTTbutton.git
``

3. Настройте параметры в коде:
```cpp
// Network settings
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "MQTT_BROKER_IP";
const char* mqtt_user = "MQTT_USERNAME";
const char* mqtt_pass = "MQTT_PASSWORD";
```

4. Прошейте вашу ESP32 любым способом
