import wmi
import pywinusb.hid as hid
from pprint import pprint


class NfcReader:
    def __init__(self, vendor_id):
        self.vendor_id = vendor_id
        self.device = None

    def connect(self):
        # Find the Baltech reader device
        devices = hid.HidDeviceFilter(vendor_id=self.vendor_id).get_devices()
        if devices:
            print("Found a match with vendorId: ", self.vendor_id)
            self.device = devices[0]

            if self.device is None:
                raise ValueError("No NFC Reader from the devices!")

            pprint(vars(self.device))

            self.device.open()
        else:
            print("No match found with vendorId: ", self.vendor_id)
            self.device = self.find_baltech_reader()

            if self.device is None:
                raise ValueError("Baltech reader not found!")

            pprint(vars(self.device))

            self.device.open()

    def find_baltech_reader(self):
        # Connect to the Windows Management Instrumentation service
        c = wmi.WMI()

        # Query for USB devices with Baltech as the manufacturer
        devices = c.Win32_USBControllerDevice()
        for device in devices:
            if self.device_manufacturer_matches(device, "Baltech"):
                return hid.HidDeviceFilter(vendor_id=self.get_vendor_product_id(device)[0],
                                           product_id=self.get_vendor_product_id(device)[1]).get_devices()[0]
        return None

    def device_manufacturer_matches(device, manufacturer_name):
        if device.Dependent:
            usb_device = device.Dependent
            print("UsbDevice manufacturer: ", usb_device.Manufacturer)
            if usb_device.Manufacturer.lower() == manufacturer_name.lower():
                return usb_device
        return None

    def get_vendor_product_id(device):
        dev_id = device.Dependent.DeviceID
        # Extract the Vendor ID (VID) and Product ID (PID) from the Device ID
        vendor_id = int(dev_id.split("VID_")[1].split("&")[0], 16)
        product_id = int(dev_id.split("PID_")[1].split("&")[0], 16)
        return vendor_id, product_id

    def disconnect(self):
        if self.device:
            self.device.close()
            self.device = None

    def read_serial_number(self):
        if self.device:
            serial_number = self.device.get_feature_report(0x0D, 20)
            return serial_number.decode('utf-8')
        else:
            raise ValueError("Baltech reader not connected.")
