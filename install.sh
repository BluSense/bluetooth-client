#!/bin/bash

echo "   ___  _             _                                          "
echo "  / __\| |__   _   _ | |  __ _                                   "
echo " / /   | '_ \ | | | || | / _\` |                                  "
echo "/ /___ | | | || |_| || || (_| |                                  "
echo "\____/ |_| |_| \__,_||_| \__,_|                                  "
echo "                                                                 "
echo "   ___  _               _                  _    _                "
echo "  / __\| | _   _   ___ | |_   ___    ___  | |_ | |__             "
echo " /__\//| || | | | / _ \| __| / _ \  / _ \ | __|| '_ \            "
echo "/ \/  \| || |_| ||  __/| |_ | (_) || (_) || |_ | | | |           "
echo "\_____/|_| \__,_| \___| \__| \___/  \___/  \__||_| |_|           "
echo "                                                                 "
echo " _                                                               "
echo "| |__   _   _                                                    "
echo "| '_ \ | | | |                                                   "
echo "| |_) || |_| |                                                   "
echo "|_.__/  \__, |                                                   "
echo "        |___/                                                    "
echo "   _    _                      _  _    _                 _       "
echo "  /_\  | |  __ _   ___   _ __ (_)| |_ | |__   _ __ ___  (_)  ___ "
echo " //_\\ | | / _\` | / _ \ | '__|| || __|| '_ \ | '_ \` _ \ | | / __|"
echo "/  _  \| || (_| || (_) || |   | || |_ | | | || | | | | || || (__ "
echo "\_/ \_/|_| \__, | \___/ |_|   |_| \__||_| |_||_| |_| |_||_| \___|"
echo "           |___/                                                 "
echo "   _____                                                         "
echo "   \_   \ _ __    ___                                            "
echo "    / /\/| '_ \  / __|                                           "
echo " /\/ /_  | | | || (__  _                                         "
echo " \____/  |_| |_| \___|(_)                                        "
echo "                                                                 "
echo "                                                                 "
echo "                                                                 "
echo "                                                                 "
echo "                                                                 "
echo "                                                                 "
echo "                                                                 "
echo ""
echo "--------------------------------------"
echo "Welcome to Chula Bluetooth scan client"
echo "--------------------------------------"
echo ""
echo "Enter your RaspberryPi device id :"
read deviceid

apt-get update -y
apt-get dist-upgrade -y
apt-get install -y bluez python-bluez python-pip screen
pip install -y requests
mkdir /srv/bt_monitor
mkdir /srv/bt_monitor/save
mkdir /srv/bt_monitor/log
cd /srv/bt_monitor
echo $deviceid >> id.txt
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/bluetooth_scan.py
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/bluetooth_scan_offline.py
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/async_datasend.py
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/check_internet.py
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/device_active.py
wget --no-check-certificate https://raw.githubusercontent.com/onnz/bluetooth-client/master/reboot_mr3020.py
(crontab -u root -l; echo "@reboot /bin/sleep 180 ; /usr/bin/python /srv/bt_monitor/bluetooth_scan_offline.py ; /sbin/reboot" ) | crontab -u root -
(crontab -u root -l; echo "@reboot /bin/sleep 200 ; /usr/bin/python /srv/bt_monitor/async_datasend.py" ) | crontab -u root -
(crontab -u root -l; echo "*/1 * * * * /usr/bin/python /srv/bt_monitor/device_active.py" ) | crontab -u root -
(crontab -u root -l; echo "*/4 * * * * /usr/bin/python /srv/bt_monitor/check_internet.py" ) | crontab -u root -
(crontab -u root -l; echo "0 2 * * * /usr/bin/python /srv/bt_monitor/reboot_mr3020.py" ) | crontab -u root -
(crontab -u root -l; echo "0 3 * * * /sbin/reboot" ) | crontab -u root -

systemctl enable ssh
timedatectl set-timezone Asia/Bangkok
apt-get install ntpdate
ntpd -gq

echo "Installing Weaved"
echo "
1
admin@ecobz.com
ThKvblue
$deviceid
1
1
y
SSH-Pi-$deviceid
4
" > /srv/bt_monitor/weaved.input
apt-get install -y weavedconnectd
weavedinstaller < /srv/bt_monitor/weaved.input

rm /srv/bt_monitor/weaved.input

echo "   ___  _         _       _     "
echo "  / __\(_) _ __  (_) ___ | |__  "
echo " / _\  | || '_ \ | |/ __|| '_ \ "
echo "/ /    | || | | || |\__ \| | | |"
echo "\/     |_||_| |_||_||___/|_| |_|"
echo "                                "

echo "Finish install RaspPi ID : "
echo $deviceid
echo ""
echo "Reboot ? (y/n) :"
read isreboot

if [ $isreboot = y ]; then
	reboot
fi
