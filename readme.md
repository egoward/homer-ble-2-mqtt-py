# What is it?

Simple python script that listens to BLE packets and relays them onto MQTT.

Learning async python project so probably terrible.  Mainly shared  so I can pull it onto devices at home without permissions faff.

Designed to run on random devices around the house so BLE range for temperature / humidity sensors isn't a problm.  Decoding the weird data formats can be done elsewhere.

# Considerations

We're just relaying one bus to another but that's a bit interesting from a privacy standpoint given anyone's data can show up.

If the messages are going to go further or be persisted messages, you need to whitelist device IDs or you're probably breaking data protection laws.

# How do you use it?

On Windows, install Python 3.X from MS store, on linux you could run:

```
sudo apt-get install python3-pip
```

Then:
```
pip3 install bleak asyncio_mqtt
```

Make sure you run it with python3.  Change the MQTT connection parameters to ones that work for you.


On a pi, give the 'pi' user access to bluetooth
```
sudo usermod -a -G bluetooth pi
sudo systemctl restart bluetooth
sudo systemctl restart dbus
```


And/or installation as a service (which runs as root).  Something like:
```
sudo cp ble2mqtt.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ble2mqtt.service
sudo systemctl start ble2mqtt.service
 ```
