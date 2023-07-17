from http.server import HTTPServer, SimpleHTTPRequestHandler
from bluepy import btle
import binascii
import struct
import math 
import pyshark
# Define the Open Drone ID service UUID
ODID_SERVICE_UUID = "00020001-0000-1000-8000-00805F9B34FB"
class ODIDScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.httpd = None

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovering")

        if isNewData:
            for (adtype, desc, value) in dev.getScanData():

                if adtype == 22 and desc == "16b Service Data":
                    print("opendroneid:", dev.addr)
                    print("16b service data", value)

                    if value.startswith("faff"):
                        print("The string starts with 'faff'")
                        service_data = binascii.unhexlify(value)
                        decode_service_data(service_data)

                        # Serve the index.html file when a device is found
                        if self.httpd is None:
                            self.httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
                            print("Serving index.html on http://localhost:8000/")
                            self.httpd.serve_forever()

                        print("Device RSSI :", dev.rssi)
                        distance = ODIDScanDelegate().estimateDistance(dev.rssi)
                        print("  Estimated distance:", distance, "meters")

                    else:
                        print("This not opendroneid data")
    def estimateDistance(self, rssi):
            # Calculate the distance based on the RSSI value using the log-distance path loss model
            # The constants used in this formula are based on empirical measurements and can vary depending on the environment
            txPower = -59 # The transmit power of the BLE device in dBm
            n = 2.0 # The path loss exponent, which depends on the environment (e.g. free space, indoors, etc.)
            return math.pow(10, (txPower - rssi) / (10 * n))   

                    
def decode_latitude(bits):
		# Convert the bits to a decimal value
		latitude_decimal = 0
		for i, bit in enumerate(bits):
			latitude_decimal += bit * 2**(23-i)

		# Convert the decimal value to degrees and decimal minutes
		latitude_degrees = latitude_decimal // 10**7
		latitude_minutes = latitude_decimal % 10**7 / 60

		return f"{latitude_degrees:.6f}, {latitude_minutes:.6f}"



	# Define the function to decode the longitude field
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
    #latitude = struct.unpack('!f', struct.pack('!I', service_data[5:9]))[0]
    #longitude = struct.unpack('!f', struct.pack('!I', service_data[9:13]))[0]
	latitude =  struct.unpack('!I',service_data[5:9])[0]
    longitude = struct.unpack('!I',service_data[9:13])[0]
    #latitude =  int.from_bytes(packet_bytes[5:9], byteorder='big', signed=True) / 10**7
    #longitude = int.from_bytes(packet_bytes[9:13], byteorder='big', signed=True) / 10**7  
	#latitude = int.from_bytes(service_data[5:9], byteorder='big', signed=True)
	#longitude = int.from_bytes(service_data[9:13], byteorder='big', signed=True)
	#latitude= service_data[5:9]
	#longitude=service_data[9:13]       
    # Convert latitude and longitude to decimal degrees with 4 decimal places
	#latitude = latitude_int / 10**7
	#longitude = longitude_int / 10**7
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
	#longitude = decode_longitude(longitude_bi



	# Print the decoded fields
	print("Open Drone ID Advertisement:")
	print(f"Message Counter: {message_counter}")
	print("Open Drone ID - Location/Vector Message")
	print(f"Message Type: Location/Vector ({message_type})")
	print(f"Protocol Version: F3411-22 ({protocol_version})")
	print(f"Operational Status: {'Airborne' if operational_status == 2 else 'Not Airborne'}")
	print(f"Height Type: {'Above Takeoff' if height_type == 0 else 'Above Ground Level'}")
	print(f"Direction: {direction}")
   
	print("Speed:", speed)
	print("Vert Speed:", vert_speed)
	print("UA Latitude:", latitude)
	print("UA Longitude:", longitude)
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





def parse_packet(packet):
    if len(packet) < 42:
        print("Invalid packet length")
        return

    # Convert the hex packet string to bytes
    packet_bytes = bytes.fromhex(packet)

    # Parse the packet according to the Open Drone ID specification
    message_counter = packet_bytes[0]
    message_type = packet_bytes[1] >> 4
    protocol_version = packet_bytes[1] & 0b00001111
    operational_status = packet_bytes[2] >> 6
    height_type = (packet_bytes[2] >> 4) & 0b00000011
    direction = packet_bytes[2] & 0b00111111
    speed = packet_bytes[3]
    vert_speed = packet_bytes[4]
   # latitude = int.from_bytes(packet_bytes[5:9], byteorder='big')
   # longitude = int.from_bytes(packet_bytes[9:13], byteorder='big')
    latitude = int.from_bytes(packet_bytes[5:9], byteorder='big', signed=True) / 10**7
    longitude = int.from_bytes(packet_bytes[9:13], byteorder='big', signed=True) / 10**7 

    pressure_altitude = int.from_bytes(packet_bytes[13:15], byteorder='big')
    geodetic_altitude = int.from_bytes(packet_bytes[15:17], byteorder='big')
    height_agl = int.from_bytes(packet_bytes[17:19], byteorder='big')
    horizontal_accuracy = packet_bytes[19] >> 4
    vertical_accuracy = packet_bytes[19] & 0b00001111
    baro_accuracy = packet_bytes[20] >> 4
    speed_accuracy = packet_bytes[20] & 0b00001111
    timestamp = int.from_bytes(packet_bytes[21:23], byteorder='big')
    timestamp_accuracy = packet_bytes[24] >> 4

    # Print the parsed data
    print("Open Drone ID Advertisement:")
    print(f"Message Counter: {message_counter}")
    print("Open Drone ID - Location/Vector Message")
    print(f"Message Type: Location/Vector ({message_type})")
    print(f"Protocol Version: F3411-22 ({protocol_version})")
    print(f"Operational Status: {'Airborne' if operational_status == 2 else 'Not Airborne'}")
    print(f"Height Type: {'Above Takeoff' if height_type == 0 else 'Above Ground Level'}")
    print(f"Direction: {direction}")
    print(f"Speed: {speed}")
    print(f"Vert Speed: {vert_speed}")
    print(f"UA Latitude: {latitude}")
    print(f"UA Longitude: {longitude}")
    print(f"UA Pressure Altitude: {pressure_altitude}")
    print(f"UA Geodetic Altitude: {geodetic_altitude}")
    print(f"UA Height AGL: {height_agl}")
    print(f"Horizontal Accuracy: <{horizontal_accuracy} m")
    print(f"Vertical Accuracy: <{vertical_accuracy} m")
    print(f"Baro Accuracy: <{baro_accuracy} m")
    print(f"Speed Accuracy: <{speed_accuracy} m/s")
    print(f"Timestamp: {timestamp}")
    print(f"Timestamp Accuracy: {timestamp_accuracy}")
    print("Reserved:", packet_bytes[23:24].hex())

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
                #parse_packet(value) 
                if value.startswith("faff"):
                    print("The string starts with 'faff'")
                    service_data = binascii.unhexlify(value)
                    decode_service_data(service_data)

                else:
                    print("This not opendroneid data")
