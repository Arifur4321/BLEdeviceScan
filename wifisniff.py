import pyshark

# Set up the Wi-Fi sniffer
capture = pyshark.LiveCapture(interface='wlan1', display_filter='wlan.fc.type_subtype == 0x08')

# Start the Wi-Fi sniffing loop
for packet in capture.sniff_continuously():

    # Check if the packet is an advertisement packet
    if 'Beacon' in packet.wlan_mgt.subtype or 'Probe Response' in packet.wlan_mgt.subtype:
        print('Advertisement packet:', packet)

        # Check if the packet has a WLAN management frame
        if hasattr(packet, 'wlan_mgt'):
            # Print out details of the advertisement packet
            print('SSID:', packet.wlan_mgt.ssid)
            print('BSSID:', packet.wlan.bssid)
            print('Signal strength:', packet.radiotap.dbm_antsignal)