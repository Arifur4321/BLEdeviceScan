from bluepy.btle import Scanner, DefaultDelegate
from geopy.geocoders import Nominatim

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            # Get the location of the device using GPS
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.reverse(f"{dev.addr}")
            print("  Latitude:", location.latitude)
            print("  Longitude:", location.longitude)
            print("  Altitude:", location.altitude)
            print("  Height:", location.raw['address']['floor'])

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data and location
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    print("  Advertising data:")
    for (adtype, desc, value) in dev.getScanData():
        print("    %s: %s" % (desc, value))
    # Get the location of the device using GPS
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{dev.addr}")
    print("  Latitude:", location.latitude)
    print("  Longitude:", location.longitude)
    print("  Altitude:", location.altitude)
    print("  Height:", location.raw['address']['floor'])