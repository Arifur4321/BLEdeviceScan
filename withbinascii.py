import binascii
import pms

# Example message value
value = "8D40621D58C382D690C8AC2863A7"

# Check if message is a Remote ID ASTM message
if value.startswith("8D4062"):
    # Convert hexadecimal message to binary
    msg_bin = binascii.unhexlify(value)

    # Decode the Remote ID message using PyModeS
    decoded = pms.adsb.gps_position(msg_bin)

    # Print the decoded message for the Remote ID ASTM message
    print(decoded)