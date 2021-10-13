Installing Arduino-Cli : 

https://siytek.com/arduino-cli-raspberry-pi/

arduino IDE install usng CLI 
sudo apt-get update && upgrade -y
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

arduino-cli
sudo nano ~/.bashrc

----- Manual Input to file ------------------

export PATH=$PATH:/home/gondola/bin
sudo reboot
arduino-cli config init

arduino-cli core install arduino:avr


arduino-cli lib install FastLED
arduino-cli lib install MFRC522

arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega /home/gondola8/blink
-----------------------------------------------------------------------------------------------------------------------------------------

Note : change gondola6 to your jetson nano username otherwise program failed to start


- cloning repo ---------------------------------------
1- sudo apt-get install git
2- git clone https://github.com/Misbahhassan08/Gondola.git

- auto start -----------------------------------------

0 - sudo apt-get update 
1- sudo apt-get upgrade -y 
2- sudo apt-get install nano
3- sudo nano /home/gondola6/startscript.sh
   // copy and paste the lines 

#!/bin/bash
/usr/bin/python3 /home/gondola6/Gondola/Finaldev.py

 // End of file here  ---- press CTRL+X , Press Y, Press Enter 

4- cd /home/gondola6/
5- sudo chmod +x startscript.sh
6- cd /home/gondola6/.config/autostart
7- sudo nano pythonscript.desktop
   
   // copy and paste lower lines in file 

[Desktop Entry]
Version=1.0
Name=Gondola
Comment=AiVision
Exec=/usr/bin/lxterminal -e /home/gondola6/startscript.sh
Icon=preferences-desktop-remote-desktop
NoDisplay=false
StartupNotify=true
Type=Application
X-GNOME-Autostart-Phase=Application
X-GNOME-AutoRestart=true
X-GNOME-UsesNotification=true

// End of file here  ---- press CTRL+X , Press Y, Press Enter

8- sudo reboot 

//------------ END -------------------------------------------------

  // IF Facing green screen issue reboot the jetson nano and start from here 
  
 1- cd /home/gondola6/jetson-inference/tools
 2- ./download-models.sh
 
  // After that de-select all options only select SSD-MOBILENET-V2 and press enter
  
  
  
  ------------------ AFTER UPDATIONs ---------------------------------------------------------------------------------------------------------------------------------
  
  Note : change gondola7 to your jetson nano username otherwise program failed to start


- cloning repo ---------------------------------------
1- sudo apt-get install git
2- git clone https://github.com/Misbahhassan08/Gondola.git  # add pip3 install pyserial
3- python3 /home/gondola7/Gondola/Finaldev.py

--- if program fails on green screen --------------------------

4- cd /home/gondola7/jetson-inference/tools
5- ./download-models.sh


 
 
