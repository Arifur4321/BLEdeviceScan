import requests
import json
from scapy.all import *

# Set your Mapbox API key token
mapbox_api_key = "sk.eyJ1IjoiYXJhaG1hbjMyMSIsImEiOiJjbGhlcHlvYWMwMTR3M25wZmJtZ3hwdWNqIn0.rU1nBTup7G13kx8nEGkE8g"

# Initialize a list to store the MAC addresses of nearby access points
nearby_macs = []

# Define a function to handle incoming WiFi packets
def handle_packet(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:
            # Add the MAC address of the access point to the list of nearby MAC addresses
            if packet.addr2 not in nearby_macs:
                nearby_macs.append(packet.addr2)

# Start capturing WiFi packets on the specified interface
sniff(iface="wlan0mon", prn=handle_packet)

# Send a POST request to the Mapbox Geolocation API with the MAC addresses of nearby access points
if nearby_macs:
    #print("Nearby MAC addresses:", nearby_macs)
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places.json?access_token=" + mapbox_api_key
    data = {
        "wifi": [{"mac": mac} for mac in nearby_macs]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        location = response.json()["features"][0]["center"]
        print("Estimated location:", location[1], location[0])
    else:
        print("Error:", response.status_code, response.text)