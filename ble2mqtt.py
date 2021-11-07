import sys, json, socket, asyncio
from bleak import BleakScanner
from asyncio_mqtt import Client

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def detection_callback(device, advertisement_data):
    global mqtt, hostname, counter

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
    await mqtt.publish("/ble/" + hostname + "/device/" + device.address,jsonText)
    counter = counter + 1

async def main():
    global mqtt, hostname, counter
    counter = 0
    hostname = socket.gethostname()

    mqtt = Client("house")
    scanner = BleakScanner(scanning_mode='passive')

    await mqtt.connect()

    await mqtt.publish("/ble/bridgerunning","yes")

    scanner.register_detection_callback(detection_callback)

    await scanner.start()
    while True:
        print("Sent BLE messages", counter)
        await asyncio.sleep(5.0)

    #This never happens!
    await scanner.stop()
   
asyncio.run(main())
