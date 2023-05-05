import requests
import json
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
import struct
import struct
import asyncio
import bleak
import time

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            # Estimate the distance based on the RSSI value
            distance = ScanDelegate().estimateDistance(dev.rssi)
            print("  Estimated distance:", distance, "meters")
            lat, lon = get_location(dev.addr)
            print("  Latitude:", lat)
            print("  Longitude:", lon)
        elif isNewData:
            print("Received new data from device:", dev.addr)


        
    def estimateDistance(self, rssi):
            # Calculate the distance based on the RSSI value using the log-distance path loss model
            # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

# Google Maps Geolocation API endpoint and API key
url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBqyGDMUcp4FZPGL6XICmX9ImxYzpIH99M"

# Function to get the latitude and longitude of a device using the Google Maps Geolocation API
def get_location(mac_address):
    # Scan for Wi-Fi access points and get their MAC addresses and signal strengths
    wifi_access_points = []
    wifi_scanner = Scanner()
    wifi_devices = wifi_scanner.scan(5.0)
    for wifi_device in wifi_devices:
        for (adtype, desc, value) in wifi_device.getScanData():
            if desc == "Complete Local Name" and value == mac_address:
                wifi_access_points.append({
                    "macAddress": wifi_device.addr.replace(":", ""),
                    "signalStrength": wifi_device.rssi
                })

    # Send a POST request to the Google Maps Geolocation API with the Wi-Fi access points and cell towers
    data = {
        "wifiAccessPoints": wifi_access_points
    }
    response = requests.post(url, data=json.dumps(data))

    # Parse the response and return the latitude and longitude
    if response.status_code == 200:
        location = response.json()["location"]
        return location["lat"], location["lng"]
    else:
        return None, None

# Function to extract the 16-bit service data from the advertising data
def get_service_data(dev):
    service_data = {}
    for (adtype, desc, value) in dev.getScanData():
        if adtype == 22:  # 16-bit service data
            uuid = value[:4]
            data = value[4:]
            service_data[uuid] = struct.unpack("<h", data)[0]
    return service_data if service_data else None



# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate())

# Continuously scan for Bluetooth devices and print out their information
while True:
    try:
        devices = scanner.scan(10.0)
        for dev in devices:
            print("Device address:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            # Estimate the distance based on the RSSI value
            distance = ScanDelegate().estimateDistance(dev.rssi)
            print("  Estimated distance:", distance, "meters")
            lat, lon = get_location(dev.addr)
            print("  Latitude:", lat)
            print("  Longitude:", lon)
            service_data = get_service_data(dev)
            if service_data:
                print("  Service data:")
                for key, value in service_data.items():
                    print("    {}: {}".format(key, value))
    except BTLEDisconnectError:
        print("Device disconnected")
    time.sleep(10)  # Delay for 10 seconds before scanning again