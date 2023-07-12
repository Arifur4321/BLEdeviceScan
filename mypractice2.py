from bluepy import btle
import binascii
import struct

# Define the Open Drone ID service UUID
ODID_SERVICE_UUID = "00020001-0000-1000-8000-00805F9B34FB"

class ODIDScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovering")

        if isNewData:
            for (adtype, desc, value) in dev.getScanData():

                if adtype == 22 and desc == "16b Service Data":
                    print("opendroneid:", dev.addr)
                    print("16b service data", value)
                    service_data = binascii.unhexlify(value)
                    decode_service_data(service_data)

def decode_latitude(bits):
    # Convert the bits to a decimal value
    latitude_decimal = 0
    for i, bit in enumerate(bits):
        latitude_decimal += bit * 2**(23-i)

    # Convert the decimal value to degrees and decimal minutes
    latitude_degrees = latitude_decimal // 10**7
    latitude_minutes = latitude_decimal % 10**7 / 60

    return f"{latitude_degrees:.6f}, {latitude_minutes:.6f}"

def decode_longitude(bits):
    # Convert the bits to a decimal value
    longitude_decimal = 0
    for i, bit in enumerate(bits):
        longitude_decimal += bit * 2**(23-i)

    # Convert the decimal value to degrees and decimal minutes
    longitude_degrees = longitude_decimal // 10**7
    longitude_minutes = longitude_decimal % 10**7 / 60

    return f"{longitude_degrees:.6f}, {longitude_minutes:.6f}"  

def decode_service_data(service_data):
    # Example decoding logic
    # Modify this based on the actual structure and format of the service data

    # Decode the fields
    message_counter = service_data[0]
    message_type = (service_data[1] & 0b11110000) >> 4
    protocol_version = service_data[1] & 0b00001111
    operational_status = (service_data[2] & 0b10000000) >> 7
    height_type = (service_data[2] & 0b01000000) >> 6
    east_west_direction = (service_data[2] & 0b00100000) >> 5
    speed_multiplier = (service_data[2] & 0b00011100) >> 2
    direction = service_data[2] & 0b00000011
    speed = service_data[3]
    vert_speed = service_data[4]
    ua_latitude = decode_latitude(service_data[5:9])
    ua_longitude = decode_longitude(service_data[9:13])
    ua_pressure_altitude = struct.unpack('!H', service_data[13:15])[0]
    ua_geodetic_altitude = struct.unpack('!H', service_data[15:17])[0]
    ua_height_agl = struct.unpack('!H', service_data[17:19])[0]
    horizontal_accuracy = (service_data[19] & 0b11110000) >> 4
    vertical_accuracy = service_data[19] & 0b00001110
    baro_accuracy = (service_data[19] & 0b00000001) << 2
    speed_accuracy = service_data[20]
    timestamp = struct.unpack('!H', service_data[21:23])[0]
    reserved = (service_data[23] & 0b11110000) >> 4
	timestamp_accuracy = service_data[23] & 0b00001111


   # Decode the latitude and longitude fields
 	#latitude_bits = service_data[5:9]
	#longitude_bits = service_data[9:13]
	#latitude = decode_latitude(latitude_bits)
	#longitude = decode_longitude(longitude_bits)

	 



	# Print the decoded fields
	print("Message Counter:", message_counter)
	print("Message Type:", message_type)
	print("Protocol Version:", protocol_version)
	print("Operational Status:", operational_status)
	print("Height Type:", height_type)
	print("East/West Direction Segment:", east_west_direction)
	print("Speed Multiplier:", speed_multiplier)
	print("Direction:", direction)
	print("Speed:", speed)
	print("Vert Speed:", vert_speed)
	print("UA Latitude:", ua_latitude)
	print("UA Longitude:", ua_longitude)
	print("UA Pressure Altitude:", ua_pressure_altitude)
	print("UA Geodetic Altitude:", ua_geodetic_altitude)
	print("UA Height AGL:", ua_height_agl)
	print("Horizontal Accuracy:", horizontal_accuracy)
	print("Vertical Accuracy:", vertical_accuracy)
	print("Baro Accuracy:", baro_accuracy)
	print("Speed Accuracy:", speed_accuracy)
	print("Timestamp:", timestamp)
	print("Reserved:", reserved)
	print("Timestamp Accuracy:", timestamp_accuracy)


# Create a scanner object and set the delegate
scanner = btle.Scanner().withDelegate(ODIDScanDelegate())

# Scan for nearby devices broadcasting ODID service UUID
devices = scanner.scan(timeout=10)

# Print the scanned devices and their service data
while True:
    devices = scanner.scan(timeout=10)

    # Print the scanned devices and their service data
    for dev in devices:
       # print("Device:", dev.addr)
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 22 and desc == "16b Service Data":
                print("opendroneid:", dev.addr)
                print("16b service data", value)
                service_data = binascii.unhexlify(value)
                decode_service_data(service_data)