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
       
            print(f"Received new data from device {dev.addr}")

            # Get the advertisement data
            adv_data = dev.getScanData()

            # Print the device information
            print(f"Device MAC address: {dev.addr}")
            print(f"Advertisement data: {adv_data}")

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data
while True:
    devices = scanner.scan(2.0)
    for dev in devices:
        print("Device address:", dev.addr)
        print("  Device name:", dev.getValueText(9))
        print("  RSSI:", dev.rssi)
        print("  Advertising data:")
        for (adtype, desc, value) in dev.getScanData():
            print("    %s: %s" % (desc, value))
           