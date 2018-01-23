#!/usr/bin/python
from hcipy import *
from signal import pause
import datetime
import time

# based on: https://github.com/sandeepmistry/node-bluetooth-hci-socket/blob/master/examples/le-scan-test.js


class BeaconScanner:

    def __init__(self, dev_id=0):
        self.hci = BluetoothHCI(dev_id)
        self.hci.on_data(self.on_data)
        self.avg_rssi = 0.0
        self.count = 0
        self.rssi_array = []
        self.set_train = False
        print(self.hci.get_device_info())
        self.found_bd_addrs = set()

    def __del__(self):
        self.hci.on_data(None)
        self.hci.stop()


    def set_filter(self):
        typeMask   = 1 << HCI_EVENT_PKT
        eventMask1 = (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
        eventMask2 = 1 << (EVT_LE_META_EVENT - 32)
        opcode     = 0

        filter = struct.pack("<LLLH", typeMask, eventMask1, eventMask2, opcode)
        self.hci.set_filter(filter)

    def set_scan_parameters(self):
        len = 7
        type = SCAN_TYPE_ACTIVE
        internal = 0x0010   #  ms * 1.6 old values 0x0010
        window = 0x0010     #  ms * 1.6 old value 0x0010
        own_addr  = LE_PUBLIC_ADDRESS
        filter = FILTER_POLICY_NO_WHITELIST
        cmd = struct.pack("<BHBBHHBB", HCI_COMMAND_PKT, LE_SET_SCAN_PARAMETERS_CMD, len,
                          type, internal, window, own_addr, filter )

        self.hci.write(cmd)


    def set_scan_enable(self, enabled=False, duplicates=False):
        len = 2
        enable = 0x01 if enabled else 0x00
        dups   = 0x01 if duplicates else 0x00
        cmd = struct.pack("<BHBBB", HCI_COMMAND_PKT, LE_SET_SCAN_ENABLE_CMD, len, enable, dups)
        self.hci.write(cmd)


    def on_data(self, data):
        if data[0] == HCI_EVENT_PKT:
            if data[1] == EVT_LE_META_EVENT:
                #print("EVT_LE_META_EVENT")
                if data[3] == EVT_LE_ADVERTISING_REPORT:
                    gap_adv_type =['ADV_IND', 'ADV_DIRECT_IND', 'ADV_SCAN_IND', 'ADV_NONCONN_IND', 'SCAN_RSP'][data[5]]
                    gap_addr_type = ['PUBLIC', 'RANDOM'][data[6]]
                    gap_addr =  [hex(c) for c in data[12:6:-1]]

                    gap_addr_str =  ':'.join([hex(c) for c in data[12:6:-1]])
                    self.found_bd_addrs.add(gap_addr_str)
                    eir = [chr(c) for c in data[14:-2]]
                    rssi = data[-1]
                    if (gap_addr_str == '0xfb:0xec:0xe:0xc5:0x58:0x14'):

                        print('LE Advertising Report')
                        '''print('\tAdv Type  = {}'.format(gap_adv_type))
                        print('\tAddr Type = {}'.format(gap_addr_type))
                        '''
                        print('\tAddr      = {}',(gap_addr_str))
                        #print('\tEIR       = {}'.format(eir))
                        print('\tRSSI      = {}'.format(rssi))
                        self.avg_rssi += rssi
                        if self.set_train:
                            self.rssi_array.append((rssi,datetime.datetime.now().time()))
                        self.count += 1
if __name__ == '__main__' :
    print "{0:=^20}".format("new iter")
    ble_scan_test = BeaconScanner()
    ble_scan_test.set_scan_enable(False)
    ble_scan_test.set_filter()
    ble_scan_test.set_scan_parameters()
    ble_scan_test.set_scan_enable(True)
    print "sleeping"
    time.sleep(20)
    print "finished"
    if 0 != ble_scan_test.count:
        print ble_scan_test.avg_rssi/ble_scan_test.count
        print ble_scan_test.count
    else:
        print 0
