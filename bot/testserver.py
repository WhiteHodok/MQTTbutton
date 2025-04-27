import socket
from config import MQTTsetting

def check_connection():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((MQTTsetting.MQTT_SERVER, 1883))
            print("✅ Соединение с сервером MQTT установлено")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    check_connection()