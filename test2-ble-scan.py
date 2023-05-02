from bluepy.btle import Scanner, DefaultDelegate

# Define a delegate class for BLE scanning
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device {dev.addr}")
        elif isNewData:
            print(f"Received new data from device {dev.addr}")

            # Parse the advertising data
            advertising_data = dev.getScanData()
            for (adtype, desc, value) in advertising_data:
                if desc == "Complete Local Name":
                    name = value
                elif desc == "Manufacturer":
                    manufacturer = value
                elif desc == "Model Number String":
                    model = value
                elif desc == "Service Data":
                    # Extract the height and location data from the service data
                    if value.startswith(b'\x00\x01'):
                        height = int.from_bytes(value[2:4], byteorder='little', signed=True)
                        latitude = int.from_bytes(value[4:8], byteorder='little', signed=True) / 1000000
                        longitude = int.from_bytes(value[8:12], byteorder='little', signed=True) / 1000000

            # Print the drone information
            print(f"Drone name: {name}")
            print(f"Drone manufacturer: {manufacturer}")
            print(f"Drone model: {model}")
            print(f"Drone height: {height}")
            print(f"Drone location: ({latitude}, {longitude})")

# Scan for BLE devices
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)