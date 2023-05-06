from bluepy.btle import Scanner, DefaultDelegate
from geopy.geocoders import Nominatim

# Define a delegate class to handle incoming BLE advertisements
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            # Get the location of the device based on its MAC address
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.geocode(dev.addr)
            if location:
                print("Device location:", location.latitude, location.longitude)
        elif isNewData:
            print("Received new data from device:", dev.addr)

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for BLE devices for 10 seconds
devices = scanner.scan(10.0)

# Print information about each discovered device
for dev in devices:
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))