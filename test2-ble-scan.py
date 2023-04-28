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

                if desc == 'Manufacturer': # Check if the advertisement data is from the manufacturer
                    if value.startswith('AER'): # Check if the manufacturer is Aerobits
                        # Decode the advertisement data based on the format provided by the manufacturer
                        data = value[3:] # Remove the Aerobits prefix
                        # Example decoding for demonstration purposes only
                        battery_level = int(data[:2], 16)
                        temperature = int(data[2:], 16) - 100
                        print("Aerobits IDME Pro advertisement data:")
                        print("  Battery level:", battery_level)
                        print("  Temperature:", temperature)
 

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
           

        if desc == 'Manufacturer': # Check if the advertisement data is from the manufacturer
                    if value.startswith('AER'): # Check if the manufacturer is Aerobits
                        # Decode the advertisement data based on the format provided by the manufacturer
                        data = value[3:] # Remove the Aerobits prefix
                        # Example decoding for demonstration purposes only
                        battery_level = int(data[:2], 16)
                        temperature = int(data[2:], 16) - 100
                        print("Aerobits IDME Pro advertisement data:")
                        print("  Battery level:", battery_level)
                        print("  Temperature:", temperature)
 
