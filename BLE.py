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
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(bytes(dev.getScanData()))

        # Print the sensor message
        print(sensor_msg)

scanner = Scanner().withDelegate(ScanDelegate())
scanner.scan(10.0) # Scan for 10 seconds