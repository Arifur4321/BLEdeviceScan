import binascii
import struct

service_data = binascii.unhexlify("faff0d6212202001fe63be0a189236cd0a98073a08e0073a63eb530100")

# Locate the positions of OperatorLatitude and OperatorLongitude
operator_latitude_start = 17
operator_longitude_start = 21

# Decode OperatorLatitude and OperatorLongitude as int32_t
operator_latitude = struct.unpack('!i', service_data[operator_latitude_start:operator_latitude_start + 4])[0]
operator_longitude = struct.unpack('!i', service_data[operator_longitude_start:operator_longitude_start + 4])[0]

# Convert latitude and longitude to floating-point values
latitude = operator_latitude / 1e7
longitude = operator_longitude / 1e7

# Print the latitude and longitude
print("Latitude:", latitude)
print("Longitude:", longitude)