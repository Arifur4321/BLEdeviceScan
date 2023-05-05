from bluepy.btle import Scanner, DefaultDelegate
from bleparser import BleParser
import requests
import json
import struct
import asyncio
import math
import time
import aioblescan as aiobs
from bleparser import BleParser
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

        # Check if the device is advertising sensor data
        if dev.getValueText(22) is not None:
            print("dev.getValueText(22) :",dev.getValueText(22))
            data = bytes.fromhex(dev.getValueText(22))
            print("data",data)
            ble_parser = BleParser()
            sensor_msg, tracker_msg = ble_parser.parse_raw_data(dev.getValueText(22))
            print("Sensor data:", sensor_msg)

 

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Continuously scan for Bluetooth devices and print out their information
while True:
    try:
        devices = scanner.scan(10.0)

    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again    