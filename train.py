from blebeacon import BeaconScanner as ble
import pickle
import time

#### Globals ####
file_name = 'node3_train.data'

if __name__ == '__main__':
    ble_scanner = ble()
    ble_scanner.set_scan_enable(False)
    ble_scanner.set_train = True
    ble_scanner.ival = 0x0010
    ble_scanner.wval = 0x0010
    ble_scanner.set_filter()
    ble_scanner.set_scan_parameters()
    ble_scanner.set_scan_enable(True)
    time.sleep(30)
    print ble_scanner.rssi_array
    f = open(file_name, 'w')
    pickle.dump(ble_scanner.rssi_array, f)
    f.close()
    exit(0)
