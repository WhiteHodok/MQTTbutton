# MQTT Button Controller with Telegram Bot Integration

![image](https://github.com/user-attachments/assets/a1032a3a-d45e-4f99-a44e-481f749e9e34)



[![GitHub stars](https://img.shields.io/github/stars/WhiteHodok/MQTTbutton?style=for-the-badge)](https://github.com/WhiteHodok/MQTTbutton)
[![ESP32](https://img.shields.io/badge/ESP32-S3-00979D?style=for-the-badge&logo=espressif)](https://www.espressif.com/)
[![MQTT](https://img.shields.io/badge/MQTT-3.1.1-660066?style=for-the-badge&logo=eclipsemosquitto)](https://mosquitto.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://python.org)

Управление физической кнопкой через MQTT с интеграцией Telegram бота. Проект позволяет отслеживать различные типы нажатий кнопки и взаимодействовать с устройством через Telegram.


![Telegram_iAWgNJROJI](https://github.com/user-attachments/assets/0ecf5158-8ef6-42b3-8174-ead5d4783af3)


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


3. Настройте параметры в коде:
```cpp
// Network settings
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "MQTT_BROKER_IP";
const char* mqtt_user = "MQTT_USERNAME";
const char* mqtt_pass = "MQTT_PASSWORD";
```

4. Прошейте вашу ESP32 любым способом.

## Для телеграм бота

1. Установите зависимости
```bash
cd root/bot

pip install -r requirements.txt
```

2. Создайте переменную среды в корне где лежит main.py
```bash
touch .env
```

3. Передайте ей атрибуты из config.py

4. Запустите вашего бота
```python
python3 main.py
```

## 🔌 Подключение компонентов

| ESP32-S3 Pin | Подключение                     |
|--------------|---------------------------------|
| GPIO35       | Кнопка (к земле через подтягивающий резистор 10кОм) |
| GPIO36 (SCL) | SCL OLED дисплея                |
| GPIO37 (SDA) | SDA OLED дисплея                |
| 3.3V         | VCC OLED дисплея                |
| GND          | GND OLED дисплея и кнопки       |

**Примечания:**
1. Для кнопки используйте подтягивающий резистор 10кОм к земле
2. OLED дисплей: SSD1306 128x64, I2C адрес 0x3C
3. Рекомендуется использовать экранированные провода для I2C


## Типы событий MQTT
```json
{
  "event": "press",
  "count": 3
}
{
  "event": "long_press"
}
{
  "event": "series_end",
  "count": 5
}
```


## Стек библиотек

ESP32:
- PubSubClient
- Adafruit_SSD1306

Python:
- aiogram 3.20
- aiomqtt 2.3.2
- pydantic 2.11.3

