#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Display settings
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C
#define SDA_PIN 37
#define SCL_PIN 36

// Button settings
#define BUTTON_PIN 35

// Network settings
const char* ssid = WIFI_SSID;
const char* password = WIFI_PASS;
const char* mqtt_server = MQTT_SERVER;
const char* mqtt_user = MQTT_USER;
const char* mqtt_pass = MQTT_PASS;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
WiFiClient espClient;
PubSubClient client(espClient);

// Button variables
int buttonPressCount = 0;
bool buttonWasPressed = false;
unsigned long lastDebounceTime = 0;
unsigned long pressStartTime = 0;
const unsigned long debounceDelay = 50;
const unsigned long multiPressThreshold = 500;
const unsigned long holdThreshold = 1000;

// Press detection variables
unsigned long lastPressTime = 0;
int pressSeriesCount = 0;
bool seriesActive = false;

// Connection status
bool wifiConnected = false;
bool mqttConnected = false;

void updateDisplay() {
  display.clearDisplay();
  display.setCursor(0, 0);
  
  // WiFi status
  display.print("WiFi: ");
  display.println(wifiConnected ? "CONNECTED" : "CONNECTING...");
  
  // MQTT status
  display.print("MQTT: ");
  display.println(mqttConnected ? "CONNECTED" : "DISCONNECTED");
  
  // Button info
  display.setCursor(0, 24);
  display.print("Total: ");
  display.print(buttonPressCount);
  
  display.setCursor(0, 36);
  display.print("Series: ");
  display.print(pressSeriesCount);
  
  display.setCursor(0, 48);
  display.print("State: ");
  display.print(buttonWasPressed ? "HOLDING" : "RELEASED");
  
  display.display();
}

void connectToWiFi() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Connecting to WiFi...");
  display.display();
  
  WiFi.begin(ssid, wifiPassword);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    display.print(".");
    display.display();
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("WiFi connected!");
    display.print("IP: ");
    display.println(WiFi.localIP());
    display.display();
    delay(1000);
  } else {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("WiFi failed!");
    display.display();
    while(1);
  }
}

void reconnectMQTT() {
  while (!client.connected()) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Connecting to MQTT...");
    display.display();
    
    if (client.connect("ESP32ButtonClient", mqttUser, mqttPassword)) {
      mqttConnected = true;
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("MQTT connected!");
      display.display();
      delay(1000);
    } else {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("MQTT failed, rc=");
      display.println(client.state());
      display.display();
      delay(5000);
    }
  }
}

void sendButtonEvent(const char* eventType, int count = 0) {
  if (!client.connected()) {
    reconnectMQTT();
  }
  
  String payload = "{\"event\":\"" + String(eventType) + "\"";
  if (count > 0) {
    payload += ",\"count\":" + String(count);
  }
  payload += "}";
  
  client.publish(mqttTopic, payload.c_str());
}

void setup() {
  Serial.begin(115200);
  
  // Initialize OLED
  Wire.begin(SDA_PIN, SCL_PIN);
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED not found!");
    while(1);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  // Initialize button
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Connect to WiFi
  connectToWiFi();
  
  // Setup MQTT
  client.setServer(mqttServer, 1883);
  reconnectMQTT();
  
  updateDisplay();
}

void loop() {
  if (!client.connected()) {
    mqttConnected = false;
    reconnectMQTT();
  }
  client.loop();
  
  bool buttonState = digitalRead(BUTTON_PIN);
  
  // Detect state changes
  if (buttonState != buttonWasPressed) {
    lastDebounceTime = millis();
  }
  
  // Process stable state
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // Button pressed (new press)
    if (buttonState == LOW && buttonWasPressed == false) {
      buttonPressCount++;
      pressStartTime = millis();
      
      // Check for series
      if (millis() - lastPressTime < multiPressThreshold) {
        pressSeriesCount++;
        seriesActive = true;
      } else {
        pressSeriesCount = 1;
      }
      lastPressTime = millis();
      
      Serial.print("Press! Total: ");
      Serial.print(buttonPressCount);
      Serial.print(" Series: ");
      Serial.println(pressSeriesCount);
      
      sendButtonEvent("press", pressSeriesCount);
      
      buttonWasPressed = true;
      updateDisplay();
    } 
    // Button released
    else if (buttonState == HIGH && buttonWasPressed == true) {
      unsigned long holdTime = millis() - pressStartTime;
      
      // Detect long press
      if (holdTime >= holdThreshold) {
        Serial.print("Long press: ");
        Serial.print(holdTime/1000.0, 1);
        Serial.println("s");
        sendButtonEvent("long_press");
      }
      
      // Reset series if timeout
      if (millis() - lastPressTime >= multiPressThreshold && seriesActive) {
        Serial.print("Series ended: ");
        Serial.print(pressSeriesCount);
        Serial.println(" presses");
        sendButtonEvent("series_end", pressSeriesCount);
        seriesActive = false;
      }
      
      buttonWasPressed = false;
      updateDisplay();
    }
  }
}