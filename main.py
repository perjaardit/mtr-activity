from device_scanner import DeviceScanner


print("************ Starting MTR activity detection ************")


# Vendor and product IDs for Baltech readers
BALTECH_VENDOR_ID = 0x04cc

scanner = DeviceScanner(BALTECH_VENDOR_ID)
scanner.start_device_activity()

print("************ Started MTR activity detection ************")