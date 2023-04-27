from bluepy.btle import Scanner, DefaultDelegate, UUID

# Define the Aerobits IDME Pro service UUID
SERVICE_UUID = UUID("0000febb-0000-1000-8000-00805f9b34fb")

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
            for (adtype, desc, value) in dev.getScanData():
                # Check if the advertising data is 16-bit service data broadcasted by Aerobits IDME Pro
                if adtype == 22 and value.startswith(SERVICE_UUID.bin()):
                    print("Received new data from device:", dev.addr)
                    # Decode the service data
                    service_data = decode_service_data(value)
                    # Print out the human-readable values
                    print("  Aerobits IDME Pro data:")
                    for key, val in service_data.items():
                        print(f"    {key}: {val}")

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


def decode_service_data(data):
    """
    Decode the 16-bit service data broadcast by Aerobits IDME Pro.

    :param data: The service data as a byte string.
    :return: A dictionary of decoded values.
    """
    decoded = {}

    # Check that the data starts with the service UUID
    if data.startswith(SERVICE_UUID.bin()):
        # Parse the values from the data
        version = data[2]
        flags = data[3]
        latitude = int.from_bytes(data[4:8], byteorder="little", signed=True) / 1e7
        longitude = int.from_bytes(data[8:12], byteorder="little", signed=True) / 1e7
        altitude = int.from_bytes(data[12:14], byteorder="little", signed=True)
        accuracy = data[14]
        num_satellites = data[15]

        # Store the values in the dictionary
        decoded["version"] = version
        decoded["flags"] = flags
        decoded["latitude"] = latitude
        decoded["longitude"] = longitude
        decoded["altitude"] = altitude
        decoded["accuracy"] = accuracy
        decoded["num_satellites"] = num_satellites

    return decoded