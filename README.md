Sudo@SDCard preparation - Rasbian installation
-----------------------------
1. Download "RASPBIAN STRETCH LITE" --> https://downloads.raspberrypi.org/raspbian_lite_latest
2. Download Etcher and install it. --> https://etcher.io/
3. Flash SDCARD
  - Connect an SD card reader with the SD card inside.
  - Open Etcher and select from your hard drive the Raspberry Pi .img or  .zip file you wish to write to the SD card.
  - Select the SD card you wish to write your image to.
  - Review your selections and click 'Flash!' to begin writing data to the SD card.
4. Plug & Run & Connect to LAN-Internet
@Raspberry Pi
-----------------------------
5. Wait for RaspberryPi finish booting
6. Login User:pi Password:raspberry
7. Type sudo su
8. Type wget -O install.sh https://goo.gl/BciKTo
9. Type chmod +x install.sh
10. Type ./install.sh
    - Define deviceid (101...102)
11. After install press y to reboot
=============================
