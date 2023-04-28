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
            print("  Advertising data:")
            for (adtype, desc, value) in dev.getScanData():
                print("   %s: %s" % (desc, value))

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
        if desc == "16b Service Data":
            # Decode the value for the specific service being advertised
            if value.startswith("aafe1716"):  # Environmental Sensing service
                temperature = int(value[10:14], 16) * 0.01
                humidity = int(value[14:18], 16) * 0.01
                print("    Temperature: %.2f °C" % temperature)
                print("    Humidity: %.2f %%" % humidity)
            else:
                print("    Unknown service data:", value)
