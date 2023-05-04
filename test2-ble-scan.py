import requests
from bluepy.btle import Scanner, DefaultDelegate

# Define a custom delegate class to handle Bluetooth device events
class ScanDelegate(DefaultDelegate):
    def __init__(self, wifi_data):
        DefaultDelegate.__init__(self)
        self.wifi_data = wifi_data

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            print("  Device name:", dev.getValueText(9))
            print("  RSSI:", dev.rssi)
            location = get_location(dev.addr, self.wifi_data)
            if location:
                print("  Location: %f, %f" % (location['lat'], location['lng']))
        elif isNewData:
            print("Received new data from device:", dev.addr)

# Initialize the Bluetooth scanner and delegate
scanner = Scanner().withDelegate(ScanDelegate([]))

# Define the Google Maps Geolocation API endpoint and API key
endpoint = "https://www.googleapis.com/geolocation/v1/geolocate"
api_key = "AIzaSyBqyGDMUcp4FZPGL6XICmX9ImxYzpIH99M"

# Define a function to scan for nearby Wi-Fi access points and collect their MAC addresses and signal strengths
def scan_wifi():
    scanner = Scanner()
    devices = scanner.scan(10.0)
    wifi_data = []
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete Local Name":
                wifi_data.append({"macAddress": dev.addr, "signalStrength": dev.rssi})
    return wifi_data

# Define a function to get the location of a device using the Google Maps Geolocation API and nearby Wi-Fi access points
def get_location(mac_address, wifi_data):
    # If there are no nearby Wi-Fi access points, scan for them and update the global wifi_data variable
    if not wifi_data:
        wifi_data = scan_wifi()

    # Look up the MAC address in the list of nearby Wi-Fi access points and send a request to the Google Maps Geolocation API to get the location
    for wifi in wifi_data:
        if wifi['macAddress'] == mac_address:
            payload = {"wifiAccessPoints": [wifi]}
            headers = {"Content-Type": "application/json", "Authorization": "key=" + api_key}
            response = requests.post(endpoint, json=payload, headers=headers)
            if response.status_code == 200:
                location = response.json()['location']
                return {"lat": location['lat'], "lng": location['lng']}

# Scan for nearby Wi-Fi access points and store the results in the wifi_data variable
wifi_data = scan_wifi()

# Initialize the Bluetooth scanner and delegate with the wifi_data variable
scanner = Scanner().withDelegate(ScanDelegate(wifi_data))

# Scan for Bluetooth devices and print out their information and location data
devices = scanner.scan(10.0)
for dev in devices:
    print("Device address:", dev.addr)
    print("  Device name:", dev.getValueText(9))
    print("  RSSI:", dev.rssi)
    location = get_location(dev.addr, wifi_data)
    if location:
        print("  Location: %f, %f" % (location['lat'], location['lng'])))