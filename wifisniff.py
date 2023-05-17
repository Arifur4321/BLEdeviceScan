import pyshark

# Set up the Wi-Fi sniffer
capture = pyshark.LiveCapture(interface='wlan1', display_filter='wlan.fc.type_subtype == 0x08 && wlan_mgt.tag_vendor_specific.oui == 0x001bc50f')

# Start the Wi-Fi sniffing loop
for packet in capture.sniff_continuously():

    print('all Wi-Fi RID packets:', packet)
    # Check if the packet is a Wi-Fi RID packet
    if 'wlan_mgt.rsn_ie' in packet:
        # Print the Wi-Fi RID details
        print('Wi-Fi RID:', packet.wlan_mgt.rsn_ie)

    # Check if the packet is an ASTM F3411 packet
    if 'btatt' in packet and packet.btatt.handle_value == '0x0025':
        # Print the ASTM F3411 details
        print('ASTM F3411:', packet.btatt.value)

    # Check if the packet is a Wi-Fi probe request packet
    if 'wlan_mgt.tag.oui' in packet and packet.wlan_mgt.tag.oui == '00:50:f2':
        # Get the MAC address of the nearby device
        mac_address = packet.wlan.ta

        # Get the latitude, longitude, and altitude of the nearby device
        latitude = packet.wlan_mgt.tag.get_field('wlan_mgt.tag.custom_data').showname_value.split(',')[0]
        longitude = packet.wlan_mgt.tag.get_field('wlan_mgt.tag.custom_data').showname_value.split(',')[1]
        altitude = packet.wlan_mgt.tag.get_field('wlan_mgt.tag.custom_data').showname_value.split(',')[2]

        # Print the nearby device details
        print('MAC Address:', mac_address)
        print('Latitude:', latitude)
        print('Longitude:', longitude)
        print('Altitude:', altitude)