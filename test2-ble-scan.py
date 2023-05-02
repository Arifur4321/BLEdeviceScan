from bluepy.btle import Scanner, DefaultDelegate, UUID

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

        # Print out advertising data, including decoded 16-bit service data
        print("  Advertising data:")
        for (adtype, desc, value) in dev.getScanData():
            print("    %s: %s" % (desc, value))
            if adtype == 22:  # 16-bit service data
                uuid = UUID(value[0:4], True)
                data = value[4:]
                print("    Decoded 16-bit service data:")
                if uuid == UUID("1809"):  # Health Thermometer service
                    temp = int.from_bytes(data, byteorder="little", signed=True) / 100
                    print("      Temperature:", temp, "°C")
                elif uuid == UUID("180D"):  # Heart Rate service
                    bpm = int.from_bytes(data, byteorder="little")
                    print("      Heart rate:", bpm, "bpm")

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices indefinitely and print out their advertising data
while True:
    devices = scanner.scan(2.0)
    for dev in devices:
        print("Device address:", dev.addr)
        print("  Device name:", dev.getValueText(9))
        print("  RSSI:", dev.rssi)