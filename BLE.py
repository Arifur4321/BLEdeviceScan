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

     def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))
       

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())
while True:
    # Scan for BLE devices for 10 seconds
    devices = scanner.scan(10.0)

    # Print information about each discovered device
    for dev in devices:

        distance = ScanDelegate().estimateDistance(dev.rssi)
        print("  Estimated distance:", distance, "meters")
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))