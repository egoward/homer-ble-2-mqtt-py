# What is it?

Simple python script that listens to BLE packets and relays them onto MQTT.

Learning async python project so probably terrible.  Mainly shared  so I can pull it onto devices at home without permissions faff.

Designed to run on random devices around the house so BLE range for temperature / humidity sensors isn't a problm.  Decoding the weird data formats can be done elsewhere.

# Considerations

We're just relaying one bus to another but that's a bit interesting from a privacy standpoint.

If the messages are going to go further or be persisted messages, you need to whitelist device IDs or you're probably breaking data protection laws.

# How do you use it?

On Windows, onstall Python 3.X from MS store, something like:

```
pip3 install bleak
pip3 install paho-mqtt
pip3 install asyncio_mqtt
```

Make sure you run it with python3

Change the MQTT connection parameters to ones that work for you.

