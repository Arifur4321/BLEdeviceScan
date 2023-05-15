import binascii
import pyModeS as pms
import bluetooth

# Continuously scan for Remote ID messages
while True:
    # Search for nearby Bluetooth devices
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        print(f"Found device {name} with MAC address {addr}")
        # Connect to the device
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((addr, 1))
        # Continuously scan for Remote ID messages
        while True:
            # Receive data from the Bluetooth socket
            data = sock.recv(1024)
            # Convert the received data from bytes to hexadecimal format
            msg_hex = binascii.hexlify(data).decode('utf-8')
            # Check if the received message is a Remote ID ASTM message
            if msg_hex.startswith('8D40'):
                # Convert the message from hexadecimal to binary format
                msg_bin = binascii.unhexlify(msg_hex)
                # Decode the Remote ID message using PyModeS
                decoded = pms.adsb.gps_position(msg_bin)
                # Print the decoded message for the Remote ID ASTM message
                print(decoded)