from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID
import math
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
            # Estimate the distance based on the RSSI value
            distance = self.estimateDistance(dev.rssi)
            print("  Estimated distance:", distance, "meters")
        elif isNewData:
            print("Received new data from device:", dev.addr)
               # Estimate the distance based on the RSSI value
            print("  RSSI:", dev.rssi)
            distance = ScanDelegate().estimateDistance(dev.rssi)

            print("  Estimated distance:", distance, "meters")

                
            print("  Advertising data:")
            for (adtype, desc, value) in dev.getScanData():
                print("    %s: %s" % (desc, value))
                
                odid_data = msgpack.unpackb(bytes.fromhex(value[10:]), raw=True)
                        # Print the decoded data
                print("ODID MessagePack data received from device:", dev.addr)
                print(odid_data)

    def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their device address, name, RSSI, and estimated distance
devices = scanner.scan(100.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    
    # Estimate the distance based on the RSSI value
    distance = ScanDelegate().estimateDistance(dev.rssi)
    print("  Estimated distance:", distance, "meters")
    
    print("  Advertising data:")
    for (adtype, desc, value) in dev.getScanData():
        print("    %s: %s" % (desc, value))
         
        odid_data = msgpack.unpackb(bytes.fromhex(value[10:]), raw=True)
                        # Print the decoded data
        print("ODID MessagePack data received from device:", dev.addr)
        print(odid_data)