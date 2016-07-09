from bluetooth import *

def getDeviceID(filename = 'id.txt'):
    # Initialization
    device_id = 9
    currentDir = os.path.dirname(os.path.realpath(__file__))
    pathfile = os.path.join(currentDir,filename)
    try:
        file = open(pathfile, "r")
        strint = file.read()
        device_id = int(strint)
    except IOError:
        device_id = 90

    return device_id

def generateRows(rawResult,addrDict = {}):
    logs,addresses = rawResult

    device_id = getDeviceID()

    def iterate(item):
        return {
            'mac_address':item[0],
            'signal':item[1],
            'device_id':device_id,
            'datetime':item[2],
            'name':addrDict.get[item[0]] if addrDict.get(item[0],None) != None else '|| None ||'
        }

    return map(iterate,logs)

def serializeJSON(data):
    return json.dumps(data)

def sendData(data,url):
    try:
        key = {'data': data}
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

        reboot = "sudo reboot"
        print('Sending {}'.format(data))
        r = requests.post(url, data=key, headers=headers)
        if r.status_code == 200:
            print("Server Side received")
        elif r.status_code == 400:
            print("Bad Request rejected by Remote Server (probably from Bad Formatting)")
        else:
            print("Server not responding to Message")
            #os.system(reboot)
            #print "reboot pi"

    except requests.ConnectionError:
        os.system("sudo reboot")

while True :
    found_device = discover_devices( duration=8, flush_cache=True )
    print(found_device)