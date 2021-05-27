import bluetooth


class BluetoothHandler:
    
    def __init__(self):
        self.prev_devices = []
        self.saved_devices = ['E4:A7:C5:B5:A8:38']
        # TODO saved devices should be dynamic
    
    def is_saved(self, device):
        if device in self.saved_devices:
            return True
        return False
    

    def detect_new_devices(self, print_devices=False):
        cur_devices = bluetooth.discover_devices(lookup_names=True)

        if print_devices:
            print("Found {} devices.".format(len(cur_devices)))
            
            for addr, name in cur_devices:
                print("  {} - {}".format(addr, name))
        
        for device in cur_devices:
            if (device not in self.prev_devices) and self.is_saved(device[0]):
                self.prev_devices = cur_devices
                return True
        
        self.prev_devices = cur_devices
        
        return False


bluetooth_handler = BluetoothHandler()