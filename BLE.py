from bluepy.btle import Scanner, DefaultDelegate
from bleparser import BleParser

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

        # Parse the advertising data using BleParser
        ble_parser = BleParser()
        for (adtype, desc, value) in dev.getScanData():
            print("    %s: %s" % (desc, value))
            data_string = value
            data = bytes(bytearray.fromhex(data_string))
            if data[0] == 255: # Check if the advertising data is manufacturer-specific
                sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
                print(sensor_msg)

scanner = Scanner().withDelegate(ScanDelegate())
scanner.scan(10.0) # Scan for 10 seconds