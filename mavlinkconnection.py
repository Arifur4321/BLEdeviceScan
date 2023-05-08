from pymavlink import mavutil

# Set the UDP port number for MAVLink communication
udp_port = 14550

# Connect to the MAVLink device using the specified UDP port
mavlink_connection = mavutil.mavlink_connection('udp:0.0.0.0:{}'.format(udp_port))

# Enable scanning mode to search for nearby devices
mavlink_connection.mav.command_long_send(
    mavlink_connection.target_system,  # Target system ID
    mavlink_connection.target_component,  # Target component ID
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # Command ID
    0,  # Confirmation
    mavutil.mavlink.MAVLINK_MSG_ID_RADIO_STATUS,  # Message ID
    1000000,  # Interval between messages (in microseconds)
    0, 0, 0, 0, 0  # Parameters (not used)
)

# Loop through each MAVLink message received from the device
while True:
    message = mavlink_connection.recv_match()
    if message:
        # Check if the message is a RADIO_STATUS message (sent by the IDME Pro)
        if message.get_type() == 'RADIO_STATUS':
            # Extract the advertising data from the message
            advertising_data = message.data

            # Print out the advertising data
            print('Advertising data:', advertising_data)