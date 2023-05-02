from bluepy.btle import Scanner, DefaultDelegate, UUID

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

        # Print out advertising data, including decoded 16-bit service data
        print("  Advertising data:")
        for (adtype, desc, value) in dev.getScanData():
            print("    %s: %s" % (desc, value))
            data = value[4:]
            uuid = UUID(value[0:4], True)
            print("data is :",  data)
            print("uuid  is :",  uuid)
            if adtype == 22:  # 16-bit service data
                uuid = UUID(value[0:4], True)
                data = value[4:]
                print("data is :",  data)
                print("    Decoded 16-bit service data:")
                if uuid == UUID("0000ffe0-0000-1000-8000-00805f9b34fb"):  # Aerobits IDME Pro service
                    if len(data) == 4:
                        # Decode the data as follows:
                        # Byte 0: Battery level (0-100%)
                        # Byte 1: Temperature (in degrees Celsius)
                        # Byte 2-3: Humidity (in %RH, little-endian)
                        battery_level = data[0]
                        temperature = data[1]
                        humidity = int.from_bytes(data[2:4], byteorder="little")
                        print("      Battery level:", battery_level, "%")
                        print("      Temperature:", temperature, "°C")
                        print("      Humidity:", humidity, "%RH")

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices indefinitely and print out their advertising data
while True:
    devices = scanner.scan(2.0)
    for dev in devices:
        print("Device address:", dev.addr)
        print("  Device name:", dev.getValueText(9))
        print("  RSSI:", dev.rssi)