from btlejack import ACLStream
from scapy.layers.bluetooth import *

# Create an ACL stream object to capture BLE packets
stream = ACLStream()

# Start capturing packets on the HCI interface
stream.start_hci_capture()

# Process incoming packets
while True:
    # Get the next packet from the stream
    packet = stream.get_packet()

    # Check if the packet is a BLE data packet
    if packet.type == ACLDataPacket:
        # Decode the packet using the scapy Bluetooth layer
        decoded_packet = Bluetooth(packet.data)

        # Print out information about the packet
        print("BLE packet received:")
        print("  Source address:", decoded_packet.src)
        print("  Destination address:", decoded_packet.dst)
        print("  Payload:", decoded_packet.payload)