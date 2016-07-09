import sys, httplib, urllib, base64
import re

def main():
	try:
		url = '192.168.0.254'
		user = 'admin'
		password = 'admin'
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

if __name__ == "__main__":
	main()