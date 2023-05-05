import requests
import json
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
import struct
import struct
import asyncio
import bleak
import time
import math
import msgpack
from newparser import BleParser

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
        elif isNewData:
            print("Received new data from device:", dev.addr)
            for (adtype, desc, value) in dev.getScanData():
                print("    %s: %s" % (desc, value))
                
              

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data
while True:
    try:
        devices = scanner.scan(10.0)
        for dev in devices:
            print("Device address:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            print("  Advertising data:")
            for (adtype, desc, value) in dev.getScanData():
                print("    %s: %s" % (desc, value))
                
    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again   