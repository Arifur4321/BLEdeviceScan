from bluepy.btle import Scanner, DefaultDelegate
from bleparser import BleParser

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
            data = bytes.fromhex(dev.getValueText(22))
            ble_parser = BleParser()
            sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
            print("Sensor data:", sensor_msg)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)