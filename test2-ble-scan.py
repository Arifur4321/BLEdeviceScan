from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import struct

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
            for (adtype, desc, value) in dev.getScanData():
                print("  Advertisement data: " + desc + " = " + self.decode_advertising_data(value))

    def decode_advertising_data(self, data):
        result = []
        index = 0
        while index < len(data):
            length = struct.unpack("B", data[index:index+1])[0]
            index += 1
            if length == 0:
                break
            adtype = struct.unpack("B", data[index:index+1])[0]
            index += 1
            if adtype == 0:
                break
            value = data[index:index+length-1]
            index += length-1
            result.append((adtype, value))
        return self.format_advertising_data(result)

def format_advertising_data(self, data):
    result = ""
    for (adtype, value) in data:
        if adtype == 1:  # Flags
            result += "Flags: " + self.format_flags(value) + "\n"
        elif adtype == 2:  # Incomplete List of 16-bit Service Class UUIDs
            result += "Incomplete List of 16-bit Service Class UUIDs: " + self.format_uuid_list(value, 2) + "\n"
        elif adtype == 3:  # Complete List of 16-bit Service Class UUIDs
            result += "Complete List of 16-bit Service Class UUIDs: " + self.format_uuid_list(value, 2) + "\n"
        elif adtype == 4:  # Incomplete List of 32-bit Service Class UUIDs
            result += "Incomplete List of 32-bit Service Class UUIDs: " + self.format_uuid_list(value, 4) + "\n"
        elif adtype == 5:  # Complete List of 32-bit Service Class UUIDs
            result += "Complete List of 32-bit Service Class UUIDs: " + self.format_uuid_list(value, 4) + "\n"
        elif adtype == 6:  # Incomplete List of 128-bit Service Class UUIDs
            result += "Incomplete List of 128-bit Service Class UUIDs: " + self.format_uuid_list(value, 16) + "\n"
        elif adtype == 7:  # Complete List of 128-bit Service Class UUIDs
            result += "Complete List of 128-bit Service Class UUIDs: " + self.format_uuid_list(value, 16) + "\n"
        elif adtype == 8:  # Shortened Local Name
            result += "Shortened Local Name: " + self.format_string(value) + "\n"
        elif adtype == 9:  # Complete Local Name
            result += "Complete Local Name: " + self.format_string(value) + "\n"
        elif adtype == 22:  # Advertising Data Type: 3D Information Data
            result += "3D Information Data: " + self.format_3d_info_data(value) + "\n"
        elif adtype == 255:  # Manufacturer Specific Data
            result += "Manufacturer Specific Data: " + self.format_manufacturer_data(value) + "\n"
        else:
            result += "Unknown Advertising Data Type " + str(adtype) + ": " + self.format_bytes(value) + "\n"
    return result

def format_flags(self, flags_byte):
    flags = ""
    if flags_byte & 0x01:
        flags += "LE Limited Discoverable, "
    if flags_byte & 0x02:
        flags += "LE General Discoverable, "
    if flags_byte & 0x04:
        flags += "BR/EDR Not Supported, "
    if flags_byte & 0x08:
        flags += "Simultaneous LE and BR/EDR to Same Device Capable (Controller), "
    if flags_byte & 0x10:
        flags += "Simultaneous LE and BR/EDR to Same Device Capable (Host), "
    return flags.rstrip(", ")

def format_uuid_list(self, uuids, size):
    result = ""
    for i in range(0, len(uuids), size):
        uuid = uuids[i:i+size][::-1]
        result += self.format_uuid(uuid) + ", "
    return result.rstrip(", ")

def format_uuid(self, uuid):
    return

