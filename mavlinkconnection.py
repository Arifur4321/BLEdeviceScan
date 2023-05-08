from bluepy.btle import Scanner, DefaultDelegate
from pymavlink import mavutil

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
        elif isNewData:
            print("Received new data from device:", dev.addr)

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Start scanning for BLE devices
devices = scanner.scan(10.0)

# Loop through each discovered device
for dev in devices:
    # Check if the device is advertising using the MAVLink protocol
    if dev.getValueText(255) and dev.getValueText(255).startswith("0x"):
        # Extract the MAC address of the device
        mac_address = dev.addr

        # Extract the signal strength of the packet
        signal_strength = dev.rssi

        # Print out information about the packet
        print("MAVLink packet received:")
        print("  MAC address:", mac_address)
        print("  Signal strength:", signal_strength)

        # Connect to the device using the MAC address
        mavlink_connection = mavutil.mavlink_connection("ble://" + mac_address)

        # Loop through each MAVLink message received from the device
        while True:
            message = mavlink_connection.recv_match()
            if message:
                # Decode the MAVLink message
                decoded_message = message.to_dict()

                # Print out information about the message
                print("MAVLink message received:")
                print("  Message ID:", decoded_message["msgid"])
                print("  Message:", decoded_message)