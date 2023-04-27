from bluepy.btle import Scanner, DefaultDelegate
import struct

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
                if desc == "Complete 16b Services":
                    # Decode the 16-bit service data as an integer
                    service_data = int(value, 16)
                    print("    Service data (hex):", value)
                    print("    Service data (int):", service_data)
                    # Extract the Remote ID message type and version from the service data
                    message_type = (service_data & 0b1111000000000000) >> 12
                    version = (service_data & 0b0000111100000000) >> 8
                    print("    Message type:", message_type)
                    print("    Version:", version)
                    # Extract the message data from the service data
                    message_data = (service_data & 0b0000000011111111)
                    if message_type == 1:
                        print("    UAS ID:", message_data)
                    elif message_type == 2:
                        print("    Location (latitude):", struct.unpack('>i', struct.pack('>I', message_data << 8))[0] / 10000000.0)
                    elif message_type == 3:
                        print("    Location (longitude):", struct.unpack('>i', struct.pack('>I', message_data << 8))[0] / 10000000.0)
                    elif message_type == 4:
                        print("    Altitude (MSL):", message_data)
                    elif message_type == 5:
                        print("    Horizontal accuracy:", message_data)
                    elif message_type == 6:
                        print("    Vertical accuracy:", message_data)
                    elif message_type == 7:
                        print("    Barometric pressure:", message_data)
                    elif message_type == 8:
                        print("    Speed:", message_data)
                    elif message_type == 9:
                        print("    Course:", message_data)
                    elif message_type == 10:
                        print("    Timestamp:", message_data)
                    elif message_type == 11:
                        print("    Emergency status:", message_data)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Aerobits IDME Pro devices and print out their advertising data
print("Scanning for Aerobits IDME Pro devices...")
devices = scanner.scan(10.0)
for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if desc == "Complete Local Name" and "IDME" in value:
            print("Aerobits IDME Pro found:")
            print("  Device address:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Complete 16b Services":
                    # Decode the 16-bit service data as an integer
                    service_data = int(value, 
