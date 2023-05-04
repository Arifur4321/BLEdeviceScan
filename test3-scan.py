from pymavlink import mavutil
from geopy.geocoders import Nominatim

# Define the MAVLink system ID and component ID
system_id = 1
component_id = 1

# Connect to the MAVLink network and wait for a heartbeat message from a nearby device
print("Connecting to MAVLink network...")
mavlink_conn = mavutil.mavlink_connection('udp:0.0.0.0:14550')
mavlink_conn.wait_heartbeat()

# Scan for nearby devices and print out their location
print("Scanning for nearby devices...")
while True:
    # Send a request to the MAVLink network to get the GPS location of nearby devices
    mavlink_conn.mav.command_long_send(
        system_id, component_id,
        mavutil.mavlink.MAV_CMD_GET_GPS_LOCATION,
        0, 0, 0, 0, 0, 0, 0, 0)

    # Wait for a GPS message from a nearby device and print out its location
    msg = mavlink_conn.recv_match(type='GPS_RAW_INT', blocking=True, timeout=10)
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1e3
        print("Device location: %f, %f, %f" % (lat, lon, alt))
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse("%f, %f" % (lat, lon))
        print("Device address:", location.address)