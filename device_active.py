import os
import sys
import requests
import json

pathfile = '/srv/bt_monitor/id.txt'

def get_id(file_name):
	try:
		file = open(file_name, "r")
		strint = file.read()
		return int(strint)
	except IOError:
		return 99
numbers = get_id(pathfile)
id = numbers

data = {'device_id': id}
headers = {'Context-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
url = 'http://data.blusense.co/activate_device.php'
r = requests.post(url, data=data, headers=headers)
print r.status_code
