from bluepy.btle import Scanner, DefaultDelegate ,BTLEDisconnectError
import struct
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

        # Check if the device is advertising ODID data
        if dev.getValueText(22) is not None:
                    data = bytes.fromhex(dev.getValueText(22))
            #  if len(data) >= 2 and data[0] == 0x0A:
                if data[1] == 0x01:
                    # Parse the ODID Decode data
                    version = data[2]
                    id_type = data[3]
                    uas_id = data[4:20].decode("utf-8").rstrip("\x00")
                    operator_location_type = data[20]
                    operator_latitude = struct.unpack("<i", data[21:25])[0] / 10**7
                    operator_longitude = struct.unpack("<i", data[25:29])[0] / 10**7
                    area_count = data[29]
                    areas = []
                    offset = 30
                    for i in range(area_count):
                        area_type = data[offset]
                        area_ceiling = struct.unpack("<H", data[offset+1:offset+3])[0] / 10
                        area_floor = struct.unpack("<H", data[offset+3:offset+5])[0] / 10
                        area_cylinder = struct.unpack("<I", data[offset+5:offset+9])[0] / 10**7
                        area_latitude = struct.unpack("<i", data[offset+9:offset+13])[0] / 10**7
                        area_longitude = struct.unpack("<i", data[offset+13:offset+17])[0] / 10**7
                        areas.append((area_type, area_ceiling, area_floor, area_cylinder, area_latitude, area_longitude))
                        offset += 17

                    # Print the parsed ODID Decode data
                    print("ODID Decode Data:")
                    print("Version:", version)
                    print("ID Type:", id_type)
                    print("UAS ID:", uas_id)
                    print("Operator Location Type:", operator_location_type)
                    print("Operator Latitude:", operator_latitude)
                    print("Operator Longitude:", operator_longitude)
                    print("Area Count:", area_count)
                    for i, area in enumerate(areas):
                        print(f"Area {i+1}:")
                        print("  Type:", area[0])
                        print("  Ceiling:", area[1])
                        print("  Floor:", area[2])
                        print("  Cylinder:", area[3])
                        print("  Latitude:", area[4])
                        print("  Longitude:", area[5])
                elif data[1] == 0x02:
                    # Parse the ODID Nominal data
                    version = data[2]
                    uid = struct.unpack("<I", data[3:7])[0]
                    timestamp = struct.unpack("<I", data[7:11])[0]
                    latitude = struct.unpack("<i", data[11:15])[0] / 10**7
                    longitude = struct.unpack("<i", data[15:19])[0] / 10**7
                    altitude = struct.unpack("<i", data[19:21])[0] / 10

                    # Print the parsed ODID Nominal data
                    print("ODID Nominal Data:")
                    print("Version:", version)
                    print("UID:", uid)
                    print("Timestamp:", timestamp)
                    print("Latitude:", latitude)
                    print("Longitude:", longitude)
                    print("Altitude:", altitude)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Continuously scan for Bluetooth devices and print out their information
while True:
    try:
        devices = scanner.scan(10.0)

    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again