import paho.mqtt.client as mqtt
import ssl
import time

# AWS IoT Core endpoint and credentials
aws_endpoint = "a12acx88i5sf07-ats.iot.us-east-1.amazonaws.com"
cert_path = "C:/Users/muzai/certs/a4539313f1b9a7e10fcdb8dd5a1af1ca985d030e12f1adca41124a6631154811-certificate.pem.crt"
key_path = "C:/Users/muzai/certs/a4539313f1b9a7e10fcdb8dd5a1af1ca985d030e12f1adca41124a6631154811-private.pem.key"
ca_path = "C:/Users/muzai/certs/AmazonRootCA1.pem"
iot_client_id = "life_pi"

# Define MQTT topic and message
mqtt_topic = "general/inbound"
message = "Bing Chilling"

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT")
        client.subscribe(mqtt_topic)
    else:
        print(f"Connection error, return code={rc}")

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, message):
    print(f"Received message on topic {message.topic}: {str(message.payload)}")

# Create an MQTT client
client = mqtt.Client(client_id=iot_client_id)
client.tls_set(ca_certs=ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to AWS IoT Core
client.connect(aws_endpoint, 8883, keepalive=60)

# Start the MQTT loop
client.loop_start()

# Publish a message
client.publish(mqtt_topic, message, qos=1)

# Wait for a few seconds to receive messages (adjust as needed)
time.sleep(5)

# Disconnect from AWS IoT
client.disconnect()