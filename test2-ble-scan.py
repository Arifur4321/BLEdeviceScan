import bluetooth
from geopy.distance import geodesic
from bluepy.btle import Scanner, DefaultDelegate

# Define a custom delegate class for handling BLE scan results
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("New Device: %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        elif isNewData:
            print("New Data for Device: %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))

# Scan for nearby Bluetooth devices using PyBluez
devices = bluetooth.discover_devices()

# Initialize the BLE scanner and set the delegate to our custom class
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for BLE devices and obtain their information
ble_devices = scanner.scan(10.0)

# Iterate through the discovered devices
for device in ble_devices:
    # Get the device's address and name
    address, name = bluetooth.lookup_name(device.addr)

    # Get the device's Bluetooth class
    device_class = bluetooth.lookup_class(device.addr)

    # Calculate the distance between the device and your location
    #  distance = geodesic((<your_latitude>, <your_longitude>, <your_altitude>), (device.addr, device.addrType, device.rssi)).meters

    # Get the device's altitude
    altitude = device.getScanData()[2][2]

    # Get the device's latitude and longitude
    manufacturer_data = device.getScanData()[3][2]
    latitude = int(manufacturer_data[2:10], 16) / 1000000.0
    longitude = int(manufacturer_data[10:18], 16) / 1000000.0

    # Print the device's information
    print("Device Name: %s" % name)
    print("Device Address: %s" % address)
    print("Device Class: %s" % device_class)
    #  print("Distance: %.2f meters" % distance)
    print("Altitude: %.2f meters" % altitude)
    print("Latitude: %.6f" % latitude)
    print("Longitude: %.6f" % longitude)
