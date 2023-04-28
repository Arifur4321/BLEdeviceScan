import msgpack

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

            # Decode MessagePack data
            for (adtype, desc, value) in dev.getScanData():
                if adtype == 255:  # Manufacturer Specific Data
                    if value.startswith(b'\x1d\xa5\x94\x01'):  # Aerobits IDME Pro
                        data = msgpack.unpackb(value[4:])
                        print("Decoded data:", data)
                        print("Altitude:", data['altitude'])
                        print("Latitude:", data['latitude'])
                        print("Longitude:", data['longitude'])
                        print("Distance:", data['distance'])
            
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
