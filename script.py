import paho.mqtt.client as mqtt
import ssl
import time
import random
import json

# AWS IoT Core endpoint and topic
AWS_ENDPOINT = 'your-aws-endpoint.iot.your-region.amazonaws.com'
MQTT_TOPIC = 'iot/dataIngestion'

# Paths to your certificate files
CERT_FILE = '/path/to/your/new-certificate.pem.crt'
KEY_FILE = '/path/to/your/new-private.pem.key'
ROOT_CA = '/path/to/AmazonRootCA1.pem'

# Define gas concentration thresholds (in ppm)
CO_THRESHOLD = 9    # CO threshold as per WHO/EPA guidelines (8-hour average)
CO2_THRESHOLD = 1000  # Comfortable indoor air quality level
PROPANE_THRESHOLD = 1000  # OSHA and NIOSH PEL for propane

# Normal ranges for gas levels in ppm
NORMAL_CO_RANGE = (0, 5)
NORMAL_CO2_RANGE = (400, 800)
NORMAL_PROPANE_RANGE = (0, 5)

# Outlier ranges for gas levels in ppm
OUTLIER_CO_RANGE = (10, 50)
OUTLIER_CO2_RANGE = (1200, 5000)
OUTLIER_PROPANE_RANGE = (1500, 5000)

# Connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core")
    else:
        print(f"Failed to connect, return code {rc}")

# Create MQTT client and set up TLS
client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs=ROOT_CA,
               certfile=CERT_FILE,
               keyfile=KEY_FILE,
               tls_version=ssl.PROTOCOL_TLSv1_2)

# Connect to AWS IoT Core
client.connect(AWS_ENDPOINT, 8883, 60)
client.loop_start()

def generate_mock_data():
    # Randomly decide if this reading will be an outlier (10% chance)
    if random.random() < 0.1:
        co_level = random.uniform(*OUTLIER_CO_RANGE)
        co2_level = random.uniform(*OUTLIER_CO2_RANGE)
        propane_level = random.uniform(*OUTLIER_PROPANE_RANGE)
    else:
        co_level = random.uniform(*NORMAL_CO_RANGE)
        co2_level = random.uniform(*NORMAL_CO2_RANGE)
        propane_level = random.uniform(*NORMAL_PROPANE_RANGE)
    
    return co_level, co2_level, propane_level


# Publish data
try:
    while True:
        co_level, co2_level, propane_level = generate_mock_data()
        payload = {
            "CO": co_level,
            "CO2": co2_level,
            "Propane": propane_level
        }
        json_payload = json.dumps(payload)
        client.publish(MQTT_TOPIC, json_payload)
        print(f"Message published: {payload}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Disconnecting from AWS IoT Core")
    client.loop_stop()
    client.disconnect()
