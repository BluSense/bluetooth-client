import os, requests, datetime
import sys, httplib, urllib, base64
import re

def check_internet(url='http://www.google.com/', timeout=5):
	try:
		req = requests.get(url, timeout=timeout)
		req.raise_for_status()
		return True
	except requests.HTTPError as e:
		print("Checking internet connection failed".format(e.response.status_cone))
	except requests.ConnectionError:
		reboot('192.168.0.254','admin','admin')
		file = open("/srv/bt_monitor/log/reboot_router.log", "a")
		file.write(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+"\n")
		file.close()
		print("No internet connection available")
	return False

def reboot(ip,user,password):
	try:
		url = ip
		user = user
		password = password
	except IndexError:
		print("No Argument supplied")
		sys.exit(2)
		
	headers = {"Cookie": "Authorization=" + urllib.quote("Basic " + base64.b64encode(user + ":" + password))}
	conn = httplib.HTTPConnection(url)
	conn.request("GET","/",None,headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	
	matchObj = re.search(r'var session_id = "(.*)";',data)
	if matchObj:
		session_id = matchObj.group(1)
	else:
		print("Session ID cannot be found")
		sys.exit(1)
	
	headers["Referer"] = "http://" + url + "/userRpm/SysRebootRpm.htm?session_id=" + session_id
	conn = httplib.HTTPConnection(url)
	conn.request("GET","/userRpm/SysRebootRpm.htm?session_id=" + session_id + "&Reboot=Reboot",None,headers)
	response = conn.getresponse()
	conn.close()

check_internet()