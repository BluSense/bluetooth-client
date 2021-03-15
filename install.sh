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

echo "Your RaspberryPi device id : "
read deviceid

echo "Is connect to Industial 4G Router? (y/n)"
read is_industialrouter

#echo "deb http://mirror1.ku.ac.th/raspbian/raspbian/ stretch main contrib non-free rpi" >> /etc/apt/sources.list
#cat /etc/apt/sources.list

apt-get update -y
apt-get dist-upgrade -y
apt-get install -y bluez python-bluez python-pip screen
pip install requests

systemctl enable ssh
timedatectl set-timezone Asia/Bangkok
apt-get install ntpdate
ntpd -gq

mkdir /srv/bt_monitor
mkdir /srv/bt_monitor/save
mkdir /srv/bt_monitor/log
cd /srv/bt_monitor

echo $deviceid >> id.txt
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/bluetooth_scan.py
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/bluetooth_scan_offline.py
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/async_datasend.py
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/check_internet.py
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/device_active.py
curl -O https://raw.githubusercontent.com/BluSense/bluetooth-client/master/reboot_mr3020.py

(crontab -u root -l; echo "@reboot /bin/sleep 180 ; /usr/bin/python /srv/bt_monitor/bluetooth_scan_offline.py ; /sbin/reboot" ) | crontab -u root -
(crontab -u root -l; echo "@reboot /bin/sleep 200 ; /usr/bin/python /srv/bt_monitor/async_datasend.py" ) | crontab -u root -
(crontab -u root -l; echo "*/1 * * * * /usr/bin/python /srv/bt_monitor/device_active.py" ) | crontab -u root -
if [ $is_industialrouter = n ]; then
	(crontab -u root -l; echo "*/4 * * * * /usr/bin/python /srv/bt_monitor/check_internet.py" ) | crontab -u root -
	(crontab -u root -l; echo "0 2 * * * /usr/bin/python /srv/bt_monitor/reboot_mr3020.py" ) | crontab -u root -
fi
(crontab -u root -l; echo "0 3 * * * /sbin/reboot" ) | crontab -u root -

echo "Setting up Dataplicity ..."

ACCT_ID="pyx825ve"
INSTALL_URL="https://www.dataplicity.com/$ACCT_ID.py | sudo python"
LOG_FILE="/var/log/mass-install-dp.log"

#Wait maximum 30 seconds on network connectivity before giving up
limit=30
retry=0



if [ ! -e /opt/dataplicity/mass-install-hostname ]; then
    echo "Configuring hostname..." >> $LOG_FILE 2>&1

    rpi_serial=$deviceid

    echo $rpi_serial | sudo tee /etc/hostname

    sed -i '$d' /etc/hosts
    printf "127.0.0.1\t$rpi_serial\n" | sudo tee --append /etc/hosts

    mkdir /opt/dataplicity
    touch /opt/dataplicity/mass-install-hostname

    echo "Rebooting..." >> $LOG_FILE 2>&1
    reboot
fi

if [ ! -e /opt/dataplicity/tuxtunnel/auth ]; then
    echo $IFACE >> $LOG_FILE 2>&1

    until ping -c 1 www.google.com > /dev/null ; do
        sleep 1
        retry=$(($retry+1))
        if [ $retry -eq $limit ]; then
            echo "Interface not connected and limit reached..." >> $LOG_FILE
            exit 0
        fi
    done

    echo "Dataplicity will now be installed..." >> $LOG_FILE 2>&1

    /bin/sh -c "curl -k $INSTALL_URL" >> $LOG_FILE 2>&1

fi

echo "   ___  _         _       _     "
echo "  / __\(_) _ __  (_) ___ | |__  "
echo " / _\  | || '_ \ | |/ __|| '_ \ "
echo "/ /    | || | | || |\__ \| | | |"
echo "\/     |_||_| |_||_||___/|_| |_|"
echo "                                "

echo "Finish install Bluetooth Sensor "
echo "Reboot ? (y/n) :"
read isreboot

if [ $isreboot = y ]; then
	reboot
fi
