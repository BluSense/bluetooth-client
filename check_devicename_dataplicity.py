import socket

def getDeviceID(filename = 'id.txt'):
    # Initialization
    device_id = "dev_id_default_id"
    currentDir = os.path.dirname(os.path.realpath(__file__))
    pathfile = os.path.join(currentDir,filename)
    try:
        file = open(pathfile, "r")
        pi_id = file.read()
        device_id = int(pi_id)
    except IOError:
        device_id = 999
    return device_id

try:
    dataplicityname_id = socket.gethostname()
    local_id = getDeviceID()

    if (local_id != 999):
        if (local_id != dataplicityname_id):
            device_id = "dev_id_default_id"
            currentDir = os.path.dirname(os.path.realpath(__file__))
            pathfile = os.path.join(currentDir,filename)
            file = open(pathfile, "w")
            file.write(str(dataplicityname_id))
            file.close()
    else:
        print("Card reading Error!!!")

except KeyboardInterrupt as e:
    print("Card reading Error!!!")
    sys.exit(1)
finally:
    sys.exit(0)
