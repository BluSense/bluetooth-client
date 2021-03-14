import os
import sys
import requests
import json

pathfile = '/srv/bt_monitor/id.txt'

def get_id(file_name):
	try:
		file = open(file_name, "r")
		pi_id = file.read()
		return int(pi_id)
	except IOError:
		return device_id = "dev_id_read_err"
numbers = get_id(pathfile)
id = numbers

data = {'device_id': id}
headers = {'Context-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
url = 'http://data.blusense.co/activate_device.php'
r = requests.post(url, data=data, headers=headers)
print r.status_code
