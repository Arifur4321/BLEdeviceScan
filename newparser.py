import asyncio
import struct
import time
import json
import msgpack
import bleak
import requests
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
import aioblescan as aiobs
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
                if desc == "Manufacturer":
                    parser.parse_manufacturer_data(value)

# Setup parser
parser = BleParser(
    discovery=False,
    filter_duplicates=True
)

# Get everything connected
loop = asyncio.get_event_loop()

#### Setup socket and controller
socket = aiobs.create_bt_socket(0)
fac = getattr(loop, "_create_connection_transport")(socket, aiobs.BLEScanRequester, None, None)
conn, btctrl = loop.run_until_complete(fac)

#### Attach callback
btctrl.process = parser.parse_raw_data
loop.run_until_complete(btctrl.send_scan_request(0))

## Run forever
loop.run_forever()