from bluepy.btle import Scanner, DefaultDelegate
from gpsd import gpsd

# Connect to the GPS module
gpsd.connect()

# Define a delegate class for BLE scanning
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device {dev.addr}")
        elif isNewData:
            print(f"Received new data from device {dev.addr}")

# Scan for BLE devices
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

# Loop through the devices and get their location
for dev in devices:
    # Check if the device is a GPS device
    if "GPS" in dev.getValueText(9):
        # Connect to the device
        print(f"Connecting to GPS device {dev.addr}")
        gps_device = dev.connect()

        # Get the GPS data
        try:
            gps_data = gpsd.get_current()
            if gps_data.mode >= 2:
                latitude = gps_data.lat
                longitude = gps_data.lon
                print(f"Device {dev.addr} location: ({latitude}, {longitude})")
            else:
                print(f"Device {dev.addr} location: Unknown")
        except Exception as e:
            print(f"Error getting GPS data for device {dev.addr}: {e}")

        # Disconnect from the device
        gps_device.disconnect()