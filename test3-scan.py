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
            # Parse the advertising data according to the ASD-STAN standard
            data = dev.getValueText(255)
            print(" ASD-STAN standard data",data)
            if data is not None:
                # Extract the data elements from the advertising data
                elements = [data[i:i+2] for i in range(0, len(data), 2)]
                i = 0
                while i < len(elements):
                    element_id = int(elements[i], 16)
                    element_len = int(elements[i+1], 16)
                    element_data = elements[i+2:i+2+element_len]
                    i += 2 + element_len
                    # Decode the data element based on its ID
                    if element_id == 0x01:
                        print("  Flags:", element_data)
                    elif element_id == 0x02:
                        print("  Incomplete List of 16-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x03:
                        print("  Complete List of 16-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x04:
                        print("  Incomplete List of 32-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x05:
                        print("  Complete List of 32-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x06:
                        print("  Incomplete List of 128-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x07:
                        print("  Complete List of 128-bit Service Class UUIDs:", element_data)
                    elif element_id == 0x08:
                        print("  Shortened Local Name:", element_data)
                    elif element_id == 0x09:
                        print("  Complete Local Name:", element_data)
                    elif element_id == 0x0a:
                        print("  TX Power Level:", element_data)
                    elif element_id == 0x0d:
                        print("  Class of Device:", element_data)
                    elif element_id == 0x16:
                        print("  Service Data:", element_data)
                    elif element_id == 0xff:
                        print("  Manufacturer Specific Data:", element_data)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Scan for Bluetooth devices and print out their advertising data
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    print("  Advertising data:")
    data = dev.getValueText(255)
    if data is not None:
        print("    Raw data:", data)