@Raspberry Pi
-----------------------------
1. Download "RASPBIAN BUSTER LITE" --> Raspberry Pi Imager
2. Or Download Etcher and install it. --> https://etcher.io/
3. Flash SDCARD
  - Connect an SD card reader with the SD card inside.
  - Open Etcher and select from your hard drive the Raspberry Pi .img or  .zip file you wish to write to the SD card.
  - Select the SD card you wish to write your image to.
  - Review your selections and click 'Flash!' to begin writing data to the SD card.
4. Plug & Run & Connect to LAN-Internet
5. Wait for RaspberryPi finish booting
6. Login User:pi Password:raspberry
7. Type sudo su
9. Type wget -O install.sh https://goo.gl/BciKTo
10. Type chmod +x install.sh
11. Type ./install.sh And Define deviceid (101...102) OR @Single Line # > 
    wget -O install.sh https://goo.gl/BciKTo && chmod +x install.sh && ./install.sh
12. After install press y to reboot


@OrangePi
-----------------------------
1. Download Debian_buster from 
    https://drive.google.com/drive/folders/1W0Bm-GGvVqgiDeSdEy_PSGlA23ahMGC6
    - Select : Orangepi4-lts_3.0.6_debian_buster_server_linux4.4.179.7z
    or
    download OPi4a ... OPi4d from github
    
    $ cat OPi4* > OPi4Image.7z

    https://drive.google.com/drive/folders/1Xk7b1jOMg-rftowFLExynLg0CyuQ7kCM
    - Select : Orangepizero2_2.2.0_debian_buster_server_linux4.9.170.7z
    or
    download OPiZero2a ... OPiZero2d from github
    
    $ cat OPiZero2* > OPiZeroImage.7z

2. Flash Download Etcher and install it. --> https://etcher.io/
3. Boot, got IP and login


@OrangePi Zero 2
-----------------------------
4. wget -O install.sh https://raw.githubusercontent.com/BluSense/bluetooth-client/master/install-orangepi.sh && chmod +x install.sh && ./install.sh

@OrangePi 4LTS
-----------------------------
4. apt-get update
5. apt-get upgrade
6. sudo nand-sata-install
    - select 2 Boot from eMMC - system on eMMC
    - select yes erase
    - select ext4
    unplug sdcard
7. wget -O install.sh https://raw.githubusercontent.com/BluSense/bluetooth-client/master/install-orangepi4lts.sh && chmod +x install.sh && ./install.sh

-----------------------------
