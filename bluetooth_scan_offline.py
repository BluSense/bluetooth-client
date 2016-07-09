import os
import sys
import datetime
import urllib2
import urllib
import httplib
import json
#import requests
#import unirest
import struct
import bluetooth._bluetooth as bluez

# --------------

def getCurrentDatetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])
    print() 

def read_inquiry_mode(sock):
    """returns the current mode, or -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # read_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # first read the current inquiry mode.
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE )

    pkt = sock.recv(255)

    status,mode = struct.unpack("xxxxxxBB", pkt)
    if status != 0: mode = -1

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return mode

def write_inquiry_mode(sock, mode):
    """returns 0 on success, -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # write_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # send the command!
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE, struct.pack("B", mode) )

    pkt = sock.recv(255)

    status = struct.unpack("xxxxxxB", pkt)[0]

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    if status != 0: return -1
    return 0

def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 8
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    logs = []
    addresses = set()

    done = False
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = struct.unpack("b", pkt[1+13*nrsp+i])[0]
                logs.append( ( addr,rssi,getCurrentDatetime() ) )
                addresses.add(addr)
                #print("[%s] RSSI: [%d]" % (addr, rssi))
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status != 0:
                print("uh oh...")
                printpacket(pkt[3:7])
                done = True
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                logs.append( ( addr, -1 ) )
                print("[%s] (no RRSI)" % addr)
        else:
            print("unrecognized packet type 0x%02x" % ptype)
        print("event ", event)

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return (logs,addresses)

def openSocket(dev_id = 0):
    try:
        sock = bluez.hci_open_dev(dev_id)
    except Exception as e:
        print("error accessing bluetooth device...")
        raise e

    try:
        mode = read_inquiry_mode(sock)
    except Exception as e:
        print("error reading inquiry mode.  ")
        print("Are you sure this a bluetooth 1.2 device?")
        print(e)
        raise e
    print("current inquiry mode is %d" % mode)

    if mode != 1:
        print("writing inquiry mode...")
        try:
            result = write_inquiry_mode(sock, 1)
        except Exception as e:
            print("error writing inquiry mode.  Are you sure you're root?")
            print(e)
            raise e
        if result != 0:
            print("error while setting inquiry mode")
        print("result: %d" % result)

    return sock

def closeSocket(sock):
    sock.close()

def getDeviceID(filename = 'id.txt'):
    # Initialization
    device_id = 90
    currentDir = os.path.dirname(os.path.realpath(__file__))
    pathfile = os.path.join(currentDir,filename)
    try:
        file = open(pathfile, "r")
        strint = file.read()
        device_id = int(strint)
    except IOError:
        device_id = 90

    return device_id

def getAddressDeviceName(sock,rawResult):
    logs,addresses = rawResult

    addrDict = {}
    timeout = int(10 * 1000)
    for addr in addresses:
        try:
            device_name = bluez.hci_read_remote_name(sock,addr,timeout)
        except bluez.error as e:
            device_name = None
        addrDict[addr] = device_name

    return addrDict

def generateRows(rawResult,addrDict = {}):
    logs,addresses = rawResult

    device_id = getDeviceID()

    def iterate(item):
        return {
            #'runloop':countLoop,
            'mac_address':item[0],
            'signal':item[1], 
            'device_id':device_id, 
            'datetime':item[2], 
            'name':addrDict.get[item[0]] if addrDict.get(item[0],None) != None else '-' 
        }

    return map(iterate,logs)

def serializeJSON(data):
    return json.dumps(data)

#runloop = 0
while True:
    try:
        #runloop = runloop + 1

        sock = openSocket()

        rawResults = device_inquiry_with_with_rssi(sock)
        rows = generateRows(rawResults)
        del rawResults

        jsonResult = serializeJSON(rows)

        if(len(rows) != 0):
            textfile_named = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            tmp_filepath = "/srv/bt_monitor/save/" + textfile_named + ".tmp"
            filepath = "/srv/bt_monitor/save/" + textfile_named + ".log"
            file = open(tmp_filepath, "w")
            file.write(jsonResult)
            file.close()
            os.rename(tmp_filepath, filepath)

        del rows
        del jsonResult

    except KeyboardInterrupt as e:
        print("Program End")
        sys.exit(0)
    finally:
        closeSocket(sock)
