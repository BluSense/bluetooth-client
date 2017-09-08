#!/bin/bash
echo ""
echo "--------------------------------------"
echo "Welcome to Chula Bluetooth scan client"
echo "--------------------------------------"
echo ""
echo "Enter your RaspPi device id :"
read deviceid

apt-get update
apt-get dist-upgrade
apt-get install bluez python-bluez python-pip screen
pip install requests
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
(crontab -u root -l; echo "@reboot /bin/sleep 60 ; /usr/bin/python /srv/bt_monitor/bluetooth_scan_offline.py ; /sbin/reboot" ) | crontab -u root -
(crontab -u root -l; echo "@reboot /bin/sleep 75 ; /usr/bin/python /srv/bt_monitor/async_datasend.py" ) | crontab -u root -
(crontab -u root -l; echo "*/1 * * * * /usr/bin/python /srv/bt_monitor/device_active.py" ) | crontab -u root -
(crontab -u root -l; echo "*/4 * * * * /usr/bin/python /srv/bt_monitor/check_internet.py" ) | crontab -u root -
(crontab -u root -l; echo "0 2 * * * /usr/bin/python /srv/bt_monitor/reboot_mr3020.py" ) | crontab -u root -
(crontab -u root -l; echo "0 3 * * * /sbin/reboot" ) | crontab -u root -

echo "Do you want to add Pi to Weaved (centralize control)? (y/n) :"
read installweaved
if [ $installweaved = y ]; then
	apt-get install weavedconnectd
	weavedinstaller
fi

echo "Finish install RaspPi ID : "
echo $deviceid
echo ""
echo "Reboot ? (y/n) :"
read isreboot

if [ $isreboot = y ]; then
	reboot
fi
