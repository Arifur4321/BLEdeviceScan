from bluepy.btle import Scanner, DefaultDelegate
import struct
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

        # Check if the device is advertising ODID nominal data
        if dev.getValueText(22) is not None:
            data = bytes.fromhex(dev.getValueText(22))
            if len(data) == 20 and data[0] == 0x0A:
                # Parse the ODID nominal data
                version = data[1]
                uid = struct.unpack("<I", data[2:6])[0]
                timestamp = struct.unpack("<I", data[6:10])[0]
                latitude = struct.unpack("<i", data[10:14])[0] / 10**7
                longitude = struct.unpack("<i", data[14:18])[0] / 10**7
                altitude = struct.unpack("<i", data[18:20])[0] / 10

                # Print the parsed data
                print("ODID Nominal Data:")
                print("Version:", version)
                print("UID:", uid)
                print("Timestamp:", timestamp)
                print("Latitude:", latitude)
                print("Longitude:", longitude)
                print("Altitude:", altitude)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Continuously scan for Bluetooth devices and print out their information
while True:
    try:
        devices = scanner.scan(10.0)

    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again