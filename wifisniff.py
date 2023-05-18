import pyshark

# Set up the Wi-Fi sniffer
capture = pyshark.LiveCapture(interface='wlan1', display_filter='wlan.fc.type_subtype == 0x08')

# Start the Wi-Fi sniffing loop
for packet in capture.sniff_continuously():

    # Check if the packet has a 16-bit service data field
    if hasattr(packet, 'wlan_mgt.tag_vendor_specific') and '16-bit Service Data' in packet.wlan_mgt.tag_vendor_specific:
        print('Wi-Fi packet with 16-bit service data:', packet)

        # Print out details of the 16-bit service data
        print('Service data:', packet.wlan_mgt.tag_vendor_specific['16-bit Service Data'])