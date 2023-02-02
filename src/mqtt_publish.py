import os
import random
import time
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as mqtt_publish
import json

load_dotenv()

mqtt_broker = os.getenv( 'MQTT_BROQUER_DIRECTION')
mqtt_port = int(os.getenv( 'MQTT_BROQUER_PORT'))
mqtt_default_topic = os.getenv('MQTT_CLIENT_DEFAULT_TOPIC')

mqtt_client_id = os.getenv('MQTT_CLIENT_ID')
mqtt_username = os.getenv('MQTT_CLIENT_USERNAME')
mqtt_password = os.getenv('MQTT_CLIENT_PASSWORD')
mqtt_keep_alive = 60


input_count_json = {"variable": "input_people", "unit": "unit", "value": random.randint(0,30)}

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code rc: " + str(rc))

#def on_connect(client, userdata, flags, rc):
#    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def run_mqtt():
    client = mqtt_client.Client()
    # Assign event callbacks
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_subscribe = on_disconnect
    
    #Connect
    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_broker, mqtt_port)
    client.loop_start()
    return client


def publish(client):
    msg = json.dumps(input_count_json)
    result = client.publish( "tago/data/post" , msg)
    status = result[0]
    if status == 0:
        print(f"Send {msg} to topic {mqtt_default_topic}")
    else:
        print(f"Failed to send message to topic {mqtt_default_topic}")


def publish_taggo(client,variable = "input_people",value = 0):
    msg_json = {"variable": variable , "unit": "unit", "value": value}
    msg = json.dumps(msg_json)
    result = client.publish(mqtt_default_topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send {msg} to topic {mqtt_default_topic}")
    else:
        print(f"Failed to send message to topic {mqtt_default_topic}")

def publish_people_in(client,value):
    publish_taggo(client,variable = "input_people",value = value)

def publish_people_out(client,value):
    publish_taggo(client,variable = "output_people",value = value)

def publish_people_into(client,value):
    publish_taggo(client,variable = "people_in_room",value = value)

def publish_taggo_single(variable = "input_people",value = 0):
    msg_json = {"variable": variable , "unit": "unit", "value": value}
    mqtt_publish.single(mqtt_default_topic, payload=json.dumps(msg_json), qos=0, retain=False, hostname=mqtt_broker,
    port=mqtt_port, client_id=mqtt_client_id, auth={'username':mqtt_username, 'password':mqtt_password}, 
    tls=None, transport="tcp")

def publish_people_in_single(value):
    publish_taggo_single(variable = "input_people",value = value)

def publish_people_out_single(value):
    publish_taggo_single(variable = "output_people",value = value)

def publish_people_into_single(value):
    publish_taggo_single(variable = "people_in_room",value = value)

#################################
# Estado del contador
# 0 todo bien   
# 1 para lleno
def publish_status(client,value = 0):
    publish_taggo(client,variable = "status",value = value)

def stop_mqtt(client):
    client.loop_stop(force=True)
    client.disconnect()



if __name__ == '__main__':
    client = run_mqtt()
    time.sleep(1)  
    publish_people_in(client,5)
    publish_people_out(client,10)
    publish_people_into(client,23)
    publish_status(client,1)
    stop_mqtt(client)
    time.sleep(1)
    print("init single_publish ")
