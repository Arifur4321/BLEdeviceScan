import aioblescan as aiobs
from bleparser import BleParser

## Setup parser
parser = BleParser(
    discovery=False,
    filter_duplicates=True
)

## Define callback
def process_hci_events(data):
    sensor_data, tracker_data = parser.parse_raw_data(data)

    if tracker_data:
        print("Tracker data:", tracker_data)

    if sensor_data:
        print("Sensor data:", sensor_data)


## Get everything connected
loop = asyncio.get_event_loop()

#### Setup socket and controller
socket = aiobs.create_bt_socket(0)
fac = getattr(loop, "_create_connection_transport")(socket, aiobs.BLEScanRequester, None, None)
conn, btctrl = loop.run_until_complete(fac)

#### Attach callback
btctrl.process = process_hci_events
loop.run_until_complete(btctrl.send_scan_request(0))

## Run forever
loop.run_forever()