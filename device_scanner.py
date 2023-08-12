import threading
import wmi

from meeting_scheduler import Scheduler
from mtr_screen import ImageShield
from nfc_reader import NfcReader


class DeviceScanner:
    def __init__(self, vendor_id):
        self.vendor_id = vendor_id
        self.nfc_reader = NfcReader(self.vendor_id)
        self.mtr_screen = ImageShield()
        self.meeting_scheduler = Scheduler(self.mtr_screen)
        self.watcher_thread = None
        self.watcher_stop_event = threading.Event()

    def start_device_activity(self):
        self.start_scan()
        self.meeting_scheduler.run()

    def start_scan(self):
        windows_interface = wmi.WMI()
        query = "SELECT * FROM __InstanceOperationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_PnPEntity'"
        watcher = windows_interface.watch_for(raw_wql=query)
        watcher.event_trigger = self.handle_device_scan

        # Create and start a separate thread for the watcher loop
        self.watcher_thread = threading.Thread(target=self.run_watcher, args=(watcher,))
        self.watcher_thread.start()

    def stop_scan(self):
        # Set the stop event to exit the watcher loop
        self.watcher_stop_event.set()

        # Wait for the watcher thread to finish
        self.watcher_thread.join()

    def run_watcher(self, watcher):
        while not self.watcher_stop_event.is_set():
            watcher(timeout_ms=500)  # Wait for events with a timeout of 500 milliseconds

    def handle_device_scan(self, event):
        # self.nfc_reader.connect()
        # try:
        #     yubikey_serial = self.nfc_reader.read_serial_number()
        #     print("Device Scanned:", event)
        print("YubiKey Serial Number:")
        #
        #     # TODO: Check the YubiKey serial number
        #
        #     self.mtr_screen.remove_shield()
        #     # TODO: Add the logic of checking if there is an ongoing meeting
        #
        # finally:
        #     self.nfc_reader.disconnect()
