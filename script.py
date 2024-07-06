import paho.mqtt.client as mqtt
import ssl
import time

# AWS IoT Core endpoint and topic
AWS_ENDPOINT = 'your-aws-endpoint.iot.your-region.amazonaws.com'
MQTT_TOPIC = 'my/iot/topic'

# Paths to your certificate files (replace with the ones obtained from the UI)
CERT_FILE = '/path/to/your/new-certificate.pem.crt'
KEY_FILE = '/path/to/your/new-private.pem.key'
ROOT_CA = '/path/to/AmazonRootCA1.pem'

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

# Publish data
try:
    while True:
        payload = '{"deviceId": "RaspberryPi", "message": "Hello from Raspberry Pi"}'
        client.publish(MQTT_TOPIC, payload)
        print(f"Message published: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Disconnecting from AWS IoT Core")
    client.loop_stop()
    client.disconnect()
