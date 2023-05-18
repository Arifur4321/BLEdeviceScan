from bluepy.btle import Scanner, DefaultDelegate, Peripheral

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
        elif isNewData:
            print("Received new data from device:", dev.addr)

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Start scanning for BLE devices
while True:
    devices = scanner.scan(10.0)

    # Print information about each discovered device
    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

        # Connect to the device and retrieve its characteristics
        try:
            peripheral = Peripheral(dev.addr, "public")
            characteristics = peripheral.getCharacteristics()

            # Read the value of each characteristic to capture packets
            for characteristic in characteristics:
                value = characteristic.read()
                print("Packet:", value)

            peripheral.disconnect()

        except:
            pass