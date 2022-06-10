# python3.6

import random

# from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt_client
from influxdb import InfluxDBClient

broker = 'localhost'
port = 1883
# topic = "python/mqtt"
topic = "ras_2"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'sensor_updates'


influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.connect(broker, port)
    client.on_connect = on_connect
    return client


def subscribe(client: mqtt_client):
    # def on_message(client, userdata, msg):
    #     print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #     json_body = [
    #     {
    #         'measurement': 'light',
    #         'tags': {
    #             'location': msg.topic
    #         },
    #         'fields': {
    #             'value': float(msg.payload.decode())
    #         }
    #     }
    #     ]
        
    def on_message_light(client,userdata,msg):
        
        print(f"Received `{msg.payload}` from `{msg.topic}` topic")
        json_body=[
        {
        'measurement':'ras_2',
        'tags':     {
                'location': msg.topic
            },
        'fields':   { 
            'light':float(msg.payload)
            }
        }
        ]
        influxdb_client.write_points(json_body)
        
    def on_message_temp(client,userdata,msg):
        print(f"Received `{msg.payload}` from `{msg.topic}` topic")
        json_body=[
        {
        'measurement':'ras_2',
        'tags':     {
                'location': msg.topic
            },
        'fields':{ 
            'temp':float(msg.payload)
            }
        }
        ]
        influxdb_client.write_points(json_body)
        
    def on_message_motion(client,userdata,msg):
        
        print(f"Received `{msg.payload}` from `{msg.topic}` topic")
        json_body=[
        {
        'measurement':'ras_2',
        'tags':     {
                'location': msg.topic
            },
        'fields':{ 'motion':float(msg.payload)}
        }
        ]
        
        influxdb_client.write_points(json_body)
    
    #influxdb_client.write_points(json_body)


    client.message_callback_add('ras_2/lab_1/light',on_message_light)
    client.message_callback_add('ras_2/lab_1/temperature',on_message_temp)
    client.message_callback_add('ras_2/lab_1/motion_sensor',on_message_motion)
    client.subscribe('ras_2/#')
    #client.on_message = on_message

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def run():
    _init_influxdb_database()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
