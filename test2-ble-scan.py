from bluepy.btle import Scanner, DefaultDelegate

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
        if dev.getValueText(9) == "Aerobits IDME Pro" and desc == "Manufacturer":
            data = bytearray.fromhex(value[4:])
            altitude = int.from_bytes(data[0:2], byteorder='big', signed=True)
            longitude = int.from_bytes(data[2:4], byteorder='big', signed=True)
            latitude = int.from_bytes(data[4:6], byteorder='big', signed=True)
            distance = int.from_bytes(data[6:8], byteorder='big', signed=False)
            print(f"      Altitude: {altitude} meters")
            print(f"      Longitude: {longitude/1000000} degrees")
            print(f"      Latitude: {latitude/1000000} degrees")
            print(f"      Distance: {distance} meters")
