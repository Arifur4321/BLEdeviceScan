from bluepy.btle import Scanner, DefaultDelegate
from opendroneid import Decoder, messages
import struct
import time

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.drones = {}

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewData:
            # Check if the device is broadcasting OpenDroneID data
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Manufacturer" and value.startswith("0x4c00"):
                    # Extract the OpenDroneID data from the advertisement data
                    data = bytes.fromhex(value[6:])
                    if len(data) >= 25 and data[0] == 0x01:
                        # Parse the OpenDroneID message
                        drone_id = struct.unpack("<H", data[1:3])[0]
                        lat = struct.unpack("<i", data[3:7])[0] / 10**7
                        lon = struct.unpack("<i", data[7:11])[0] / 10**7
                        alt = struct.unpack("<h", data[11:13])[0] / 10
                        accuracy_h = struct.unpack("<H", data[13:15])[0] / 10
                        accuracy_v = struct.unpack("<H", data[15:17])[0] / 10
                        speed = struct.unpack("<H", data[17:19])[0] / 10
                        heading = struct.unpack("<H", data[19:21])[0] / 100
                        timestamp = struct.unpack("<I", data[21:25])[0]

                        # Add the drone to the list of detected drones
                        self.drones[drone_id] = (lat, lon, alt)

                        # Print the drone location and OpenDroneID data
                        print(f"Drone {drone_id} location: ({lat}, {lon}, {alt})")
                        print(f"OpenDroneID data: accuracy_h={accuracy_h}, accuracy_v={accuracy_v}, speed={speed}, heading={heading}, timestamp={timestamp}")

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Initialize the OpenDroneID decoder
decoder = Decoder()

# Scan for Bluetooth devices and print out their OpenDroneID data
while True:
    devices = scanner.scan(2.0)
    for dev in devices:
        # Decode any OpenDroneID messages received from the device
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Manufacturer" and value.startswith("0x4c00"):
                data = bytes.fromhex(value[6:])
                if len(data) >= 25 and data[0] == 0x01:
                    message = decoder.decode(data)
                    if isinstance(message, messages.BasicID):
                        print(f"Received BasicID message from drone {message.ID}")
                    elif isinstance(message, messages.Location):
                        print(f"Received Location message from drone {message.ID}: ({message.Latitude}, {message.Longitude}, {message.Altitude})")
                    elif isinstance(message, messages.Auth):
                        print(f"Received Auth message from drone {message.ID}")
                    elif isinstance(message, messages.SelfID):
                        print(f"Received SelfID message from drone {message.ID}")
                    elif isinstance(message, messages.System):
                        print(f"Received System message from drone {message.ID}")
                    elif isinstance(message, messages.OperatorID):
                        print(f"Received OperatorID message from drone {message.ID}")
                    elif isinstance(message, messages.MessagePack):
                        print(f"Received MessagePack message from drone {message.ID}")
                    else:
                        print(f"Received unknown message type from drone {message.ID}")

        # Print the list of detected drones
        if dev.addrType == "public":
            print(f"Detected drones: {scan_delegate.drones}")

    # Wait for a few seconds before scanning again
    time.sleep(2)