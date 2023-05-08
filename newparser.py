import requests
import json
from bluepy.btle import Scanner, DefaultDelegate
import math 

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
            # Add the MAC address of the device to a list of nearby MAC addresses
            nearby_macs.append(dev.addr)
        elif isNewData:
            print("Received new data from device:", dev.addr)

    def estimateDistance(self, rssi):
        # Calculate the distance based on the RSSI value using the log-distance path loss model
        # The constants used in this formula are based on empirical measurements and can vary depending on the environment
        txPower = -59 # The transmit power of the BLE device in dBm
        n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
        return math.pow(10, (txPower - rssi) / (10 * n))

# Create a scanner object and set the delegate to handle incoming advertisements
scanner = Scanner().withDelegate(ScanDelegate())

# Initialize a list to store the MAC addresses of nearby devices
nearby_macs = []

# Set up the OpenCageData API credentials
api_key = "f940ee19fdd24a87a0e48f8523e1cec1"

while True:
    # Scan for BLE devices for 10 seconds
    devices = scanner.scan(10.0)

    # Print information about each discovered device
    for dev in devices:
        distance = ScanDelegate().estimateDistance(dev.rssi)
        print("  Estimated distance:", distance, "meters")
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

    # Send a GET request to the OpenCageData API with the MAC addresses of nearby devices
    if nearby_macs:
        print ("nearby mac :",nearby_macs)
        url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            "key": api_key,
            "macs": ",".join(nearby_macs)
        }
        print ("params :",params)
        response = requests.get(url, params=params)
        print ("response :",response)
        if response.status_code == 200:
            results = response.json()["results"]
            for result in results:
                location = result["geometry"]
                print("MAC address:", result["annotations"]["mac"]["address"])
                print("  Latitude:", location["lat"])
                print("  Longitude:", location["lng"])
        else:
            print("Error:", response.status_code, response.text)
    else:
        print("No nearby devices found")

    # Clear the list of nearby MAC addresses for the next scan
    nearby_macs = []