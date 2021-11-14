import sys, json, socket, asyncio, time
from bleak import BleakScanner
import asyncio_mqtt
import paho.mqtt.client as mqtt


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class BLE2MQTT:
  def __init__(self):
    self.x=3
    print("Hello")
    self.counter = 0
    self.hostname = socket.gethostname()
    self.conn = asyncio_mqtt.Client("House")
    self.last_connect_time = 0
    self.reconnect_interval_seconds = 10
    self.heartbeat_interval_seconds = 60
    self.scanner = BleakScanner(scanning_mode='passive')
    self.scanner.register_detection_callback(self.detection_callback)
  
  async def start(self):
    await self.maybe_connect()
    asyncio.get_event_loop().create_task(self.heartbeat())
    await self.scanner.start()

  async def maybe_connect(self):
    if time.time() - self.last_connect_time < self.reconnect_interval_seconds:
      return  
    print("Connecting to MQTT")
    try:
      self.last_connect_time = time.time()
      await self.conn.connect()
      print("Connected")
    except BaseException as eConn:
      print("Error Connecting : ", eConn)

  async def try_send(self, subject, message):
    print("Message for ", subject, " : " , message)
    try:
      await self.conn.publish(subject, message)
    except  asyncio_mqtt.error.MqttCodeError as ePub:
      print("Error sending message :  ", ePub)
      if ePub.rc is mqtt.MQTT_ERR_NO_CONN:
        await self.maybe_connect()

  async def detection_callback(self,device, advertisement_data):
      global conn, hostname, counter
      manufacturer = []
      for key, value in advertisement_data.manufacturer_data.items():
          manufacturer.append( {'company':key, 'data':value.hex()} )
      service = {}
      for key, value in advertisement_data.service_data.items():
          service[ key ] = value.hex()
      obj4json = {
          'name':device.name,
          'manufacturer' : manufacturer,
          'service' : service,
          'service_uuids' : advertisement_data.service_uuids
      }
      jsonText = json.dumps(obj4json)
      await self.try_send("ble/" + self.hostname + "/device/" + device.address,jsonText)
      self.counter = self.counter + 1

  async def heartbeat(self):
    while True:
      await self.try_send("ble/"+self.hostname+"/status",json.dumps({'sent':self.counter}))
      await asyncio.sleep(self.heartbeat_interval_seconds)


async def main():
    ble2mqtt = BLE2MQTT()
    await ble2mqtt.start()

    while True:
        print("Main loop ticking away")
        await asyncio.sleep(60.0)

asyncio.run(main())
