import asyncio
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

remote_url = "mqtt://test.mosquitto.org:1883/"
topic = "testtopic/testtest"
msgdata = b'Hello'

async def main():
    b = MQTTClient(config={'keep_alive': 60})
    await b.connect(remote_url)
    while True:
        await asyncio.sleep(5)
        asyncio.create_task(b.publish(topic=topic, message=msgdata, qos=QOS_1))

if __name__ == '__main__':
    asyncio.run(main())