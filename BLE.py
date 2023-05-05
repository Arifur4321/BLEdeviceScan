from bleparser import BleParser
from scapy.all import *
from bleparser import BleParser

# Define the BLE and Wi-Fi sniffing functions
def ble_sniff(pkt):
    if pkt.haslayer(ScanResponse):
        data = bytes(pkt.getlayer(ScanResponse).payload)
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)
        print("BLE Sensor Message:", sensor_msg)

def wifi_sniff(pkt):
    if pkt.haslayer(Dot11ProbeResp):
        print("Wi-Fi Probe Response:", pkt.summary())

# Start the BLE and Wi-Fi sniffers
sniff(prn=ble_sniff, filter="type mgt and subtype beacon", iface="wlan0mon")
sniff(prn=wifi_sniff, filter="type mgt and subtype probe-resp", iface="wlan0mon")


 