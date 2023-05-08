from bluepy.btle import Scanner, DefaultDelegate
from scapy.all import *

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
        elif isNewData:
            print("Received new data from device:", dev.addr)

def handle_wifi_packet(packet):
    if packet.haslayer(Dot11):
        # Extract the MAC address of the access point and the client device
        ap_mac = packet.addr2
        client_mac = packet.addr1

        # Extract the signal strength of the packet
        signal_strength = packet.dBm_AntSignal

        # Print out information about the packet
        print("WiFi packet received:")
        print("  Access point MAC:", ap_mac)
        print("  Client device MAC:", client_mac)
        print("  Signal strength:", signal_strength)

def handle_bluetooth_packet(packet):
    if packet.haslayer(BLE_ADvertising):
        # Extract the MAC address of the Bluetooth device
        mac_address = packet.addr

        # Extract the signal strength of the packet
        signal_strength = packet.dBm

        # Print out information about the packet
        print("Bluetooth packet received:")
        print("  MAC address:", mac_address)
        print("  Signal strength:", signal_strength)

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Start capturing packets on the WiFi and Bluetooth interfaces
sniff(iface="wlan0", prn=handle_wifi_packet)
sniff(iface="hci0", prn=handle_bluetooth_packet)

while True:
    # Scan for BLE devices for 10 seconds
    devices = scanner.scan(10.0)

    # Print information about each discovered device
    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))