import msgpack
from bluepy.btle import Scanner, DefaultDelegate, UUID
import binascii

# Define the UUID of the Aerobits IDME Pro service
AEROBITS_SERVICE_UUID = UUID("58da3605-5d5e-11e9-8647-d663bd873d93")

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

            # Check if the service data belongs to the Aerobits IDME Pro device
            service_data = None
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 22 and desc.startswith('16b Service Data'):
                    service_data = value
                    break
            if service_data is not None:
                uuid = binascii.unhexlify(service_data[0:4])[::-1]  # reverse byte order
                if uuid == bytes(AEROBITS_SERVICE_UUID):
                    # Parse the Aerobits IDME Pro advertising data
                    altitude = int.from_bytes(service_data[5:7], byteorder='big', signed=True) * 0.1
                    latitude = int.from_bytes(service_data[7:11], byteorder='big', signed=True) * 0.0001
                    longitude = int.from_bytes(service_data[11:15], byteorder='big', signed=True) * 0.0001
                    distance = int.from_bytes(service_data[15:17], byteorder='big', signed=True) * 0.1
                    print("Decoded data:")
                    print("  Altitude:", altitude)
                    print("  Latitude:", latitude)
                    print("  Longitude:", longitude)
                    print("  Distance:", distance)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    print("  Advertising data:")
    for (adtype, desc, value) in dev.getScanData():
        print("    %s: %s" % (desc, value))
