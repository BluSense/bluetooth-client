# performs a simple device inquiry, followed by a remote name request of each
# discovered device

import os
#import os.path
import sys
import struct
import bluetooth._bluetooth as bluez
import bluetooth
import datetime
import urllib2
import urllib
import httplib
import json
import requests

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
	#id = os.getenv('BT_ID',90)
	id = 90
	pathfile = 'id.txt'
	#path_logfile = '/home/pi/bt_logfile.txt'	
	try:
		file = open(pathfile, "r")
		strint = file.read()
		id = int(strint)
	except IOError:
		id = 90

	while True:
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
		duration = 1
		max_responses = 255 
		cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
		bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

		
		#results = []
		try:
			pkt = sock.recv(255)
			ptype, event, plen = struct.unpack("BBB", pkt[:3])
			if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
			    pkt = pkt[3:]
			    nrsp = struct.unpack("B", pkt[0])[0]
			    device_id = id
			    tf = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			    
			    for i in range(nrsp):
				addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
				rssi = struct.unpack("b", pkt[1+13*nrsp+i])[0]
				name = bluetooth.lookup_name(addr)
				#results.append( (name, addr, rssi, device_id, tf) )
				data = [{'mac_address':addr, 'signal':rssi, 'device_id':device_id, 'datetime':tf, 'name':name}]
				key = {'data': json.dumps(data)}	
				headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
				#print data_string
				url = 'http://61.19.50.165/Bluetooth.php'
				#url = 'http://bluetoothbe.mybluemix.net/Bluetooth.php'
				#logfile = open(path_logfile, 'a')
				reboot = "sudo reboot"
				if name != 'raspberrypi-0':
					#logfile.write(str(data)+'\n')
					print('Sending {}'.format(json.dumps(data)))
					r = requests.post(url, data=key, headers=headers)
					if r.status_code == 200:
						print("Server Side received")
					elif r.status_code == 400:
						print("Bad Request rejected by Remote Server (probably from Bad Formatting)")
					else:
						print("Server not responding to Message")
						#os.system(reboot)
						#print "reboot pi"
				else:
					None	
			# restore old filter
			sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

		except requests.ConnectionError:
			os.system("sudo reboot")


dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("error accessing bluetooth device...")
    sys.exit(1)

try:
    mode = read_inquiry_mode(sock)
except Exception as e:
    print("error reading inquiry mode.  ")
    print("Are you sure this a bluetooth 1.2 device?")
    print(e)
    sys.exit(1)
#print("current inquiry mode is %d" % mode)

if mode != 1:
    print("writing inquiry mode...")
    try:
        result = write_inquiry_mode(sock, 1)
    except Exception as e:
        print("error writing inquiry mode.  Are you sure you're root?")
        print(e)
        sys.exit(1)
    if result != 0:
        print("error while setting inquiry mode")
    print("result: %d" % result)

try:
	device_inquiry_with_with_rssi(sock)
except Exception as e:
	print e
	sys.exit(1)
