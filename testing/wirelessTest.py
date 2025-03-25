import network
import time
import ubinascii
import machine
from simple import MQTTClient

# WiFi and MQTT Broker settings
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()
TOPIC = "esp/button"

# Setup WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("Connected to WiFi")

# MQTT Callback function
def on_message(topic, msg):
    print(f"Received message: {msg.decode()} on topic: {topic.decode()}")
    if msg == b'ON':
        led.value(1)  # Turn LED ON
    elif msg == b'OFF':
        led.value(0)  # Turn LED OFF

# Initialize MQTT Client
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC)
print(f"Subscribed to topic {TOPIC}")

# LED Setup
led = machine.Pin(25, machine.Pin.OUT)  # Change GPIO as needed

# Main loop to check for messages
while True:
    try:
        client.check_msg()  # Check for new MQTT messages
    except Exception as e:
        print(f"MQTT Error: {e}")
        client.connect()
        client.subscribe(TOPIC)
    time.sleep(0.1)
