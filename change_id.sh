#!/bin/bash

echo "--------------------------------------"
echo "Welcome to Chula Bluetooth scan client"
echo "--------------------------------------"
echo ""

cd /srv/bt_monitor
current_id=$(<id.txt)

echo "Your current RaspberryPi ID is : "
echo $current_id
echo ""
echo "Do you want change to : "
read deviceid

echo "Changing ID & Configuring hostname..."
echo $deviceid | tee /etc/hostname
echo $deviceid | tee id.txt

sed -i '$d' /etc/hosts
printf "127.0.0.1\t$deviceid\n" | tee --append /etc/hosts
hostnamectl set-hostname $deviceid
systemctl restart avahi-daemon

echo "Finish install new ID "
echo "Reboot ? (y/n) :"
read isreboot

if [ $isreboot = y ]; then
	reboot
fi
