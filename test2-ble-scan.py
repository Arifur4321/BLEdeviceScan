import gps
from bluetooth import discover_devices, BluetoothError

# Connect to the GPS module
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Define a function to get the GPS data
def get_gps_data():
    try:
        report = session.next(timeout=1)
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                latitude = report.lat
                longitude = report.lon
                return (latitude, longitude)
    except Exception as e:
        print(e)
    return None

# Discover nearby Bluetooth devices that support SPP
devices = discover_devices(lookup_names=True, lookup_class=True)
spp_devices = []
for device, name, device_class in devices:
    if device_class[0] == 0x01 and device_class[1] == 0x00 and device_class[2] == 0x00:
        spp_devices.append((device, name))

# Loop through the devices and get their location
for device, name in spp_devices:
    # Get the latitude and longitude of the device
    location = get_gps_data()

    # Print the device name and location
    if location is not None:
        print(f"Device: {name}, Location: ({location[0]}, {location[1]})")
    else:
        print(f"Device: {name}, Location: Unknown")