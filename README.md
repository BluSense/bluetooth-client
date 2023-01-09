Sudo@SDCard preparation - Rasbian installation
-----------------------------
1. Download "RASPBIAN BUSTER LITE" --> Raspberry Pi Imager
2. Or Download Etcher and install it. --> https://etcher.io/
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
9. Type wget -O install.sh https://goo.gl/BciKTo
10. Type chmod +x install.sh
11. Type ./install.sh And Define deviceid (101...102) OR @Single Line # > 
    wget -O install.sh https://goo.gl/BciKTo && chmod +x install.sh && ./install.sh

12. After install press y to reboot
=============================


@Orange Pi
1. Download Debian_buster from https://drive.google.com/drive/folders/1W0Bm-GGvVqgiDeSdEy_PSGlA23ahMGC6
    - Select from Backup : Orangepi4-lts_3.0.2_debian_buster_server_linux4.4.179.7z
2. Flash Download Etcher and install it. --> https://etcher.io/
3. Boot, got IP and login

@ORANGEPI 4LTS
4. apt-get update
5. apt-get upgrade
6. sudo nand-sata-install
    - select 2 Boot from eMMC - system on eMMC
    - select yes erase
    - select ext4
-----------------------------
Burn SDCARD
- https://drive.google.com/file/d/1N0A5XS4POfX-tSzOihvoxIdLMZqz1xJ6/view?usp=share_link

- ORANGEPI ZERO2

    - wget -O install.sh https://raw.githubusercontent.com/BluSense/bluetooth-client/master/install-orangepi.sh && chmod +x install.sh && ./install.sh

- ORANGEPI 4LTS

    - wget -O install.sh https://raw.githubusercontent.com/BluSense/bluetooth-client/master/install-orangepi4lts.sh && chmod +x install.sh && ./install.sh