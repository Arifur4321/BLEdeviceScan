# Getting "advertisingData" before via the BLE

from bleAdvReader import BLEAdvReader

advReader = BLEAdvReader(advertisingData)

# Gets the service data part in the advertising packet,
svcData = advReader.GetDataByDataType(BLEAdvReader.DATA_TYPE_SVC_DATA)

# List all decoded and structured objects (class),
for advElement in advReader.GetAllElements() :
    print(advElement)
    # Finds an iBeacon with classes instances comparison,
    if isinstance(advElement, BLEAdvReader.AppleIBeacon) :
    	print('This is an iBeacon with UUID %s' % advElement.StrUUID)

# Gets the same iBeacon more directly,
iBeaconElement = advReader.GetElementByClass(BLEAdvReader.AppleIBeacon)
if iBeaconElement :
	print('iBeacon found!')