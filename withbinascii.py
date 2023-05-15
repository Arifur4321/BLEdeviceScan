import binascii
import pyModeS as pms

# Sample Remote ID astm message in hexadecimal format 
msg_hex = "8D40621D58C382D690C8AC2863A7"

# Convert message from hexadecimal to binary
msg_bin = binascii.unhexlify(msg_hex)

# Decode Remote ID message using PyModeS
decoded = pms.cat21.decode(msg_bin)

# Print the decoded message for astm
print(decoded)