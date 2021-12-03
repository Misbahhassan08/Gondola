from pathlib import Path
from os import path
import os 
import time 
def update_git():
    HOME_DIR = Path.home()
    os.system('cd {}/ && git sudo reset --hard'.format(HOME_DIR))
    os.system('cd {}/ && git sudo clean -df'.format(HOME_DIR))
    os.system('cd {}/ && git sudo pull -f'.format(HOME_DIR))

def install_dep():
    HOME_DIR = Path.home()



    os.system('sudo apt-get update')
    os.system('sudo apt-get install git cmake libpython3-dev python3-numpy python3-pip nano python3-scipy python3-h5py python3-pil curl -y')
    os.system('sudo pip3 install screeninfo')

    # ----------------- auto start script -----------------------------------------------------------------
    script_file = '{}/startscript.sh'.format(HOME_DIR)
    if (path.exists(script_file) == False):
        outFileName = '{}/startscript.sh'.format(HOME_DIR)
        outFile=open(outFileName, "w")
        outFile.write("""
#!/bin/bash
/usr/bin/python3 {}/Gondola/Finaldev.py
        """.format(HOME_DIR))
        outFile.close()
        os.system('sudo chmod +x {}/startscript.sh'.format(HOME_DIR))
        pass
    

    outFileName = '{}/.config/autostart/pythonscript.desktop'.format(HOME_DIR)
    if (path.exists(outFileName) == False):
        outFileName = '{}/.config/autostart/pythonscript.desktop'.format(HOME_DIR)
        outFile=open(outFileName, "w")
        outFile.write("""
[Desktop Entry]
Version=1.0
Name=Gondola
Comment=AiVision
Exec=/usr/bin/lxterminal -e {}/startscript.sh
Icon=preferences-desktop-remote-desktop
NoDisplay=false
StartupNotify=true
Type=Application
X-GNOME-Autostart-Phase=Application
X-GNOME-AutoRestart=true
X-GNOME-UsesNotification=true
        """.format(HOME_DIR))
        outFile.close()
        pass

    v = str(input('press a to restart b to continue'))
    if v == "a" or v == "A":
        os.system('sudo reboot')
    os.system('cd {} && git clone --recursive https://github.com/dusty-nv/jetson-inference'.format(HOME_DIR))
    os.system('mkdir {}/jetson-inference/build'.format(HOME_DIR))

    os.system('cd {}/jetson-inference/build && sudo cmake ../'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo make -j$(nproc)'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo make install'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo ldconfig'.format(HOME_DIR))


    # ----------------- installing pillow -----------------

    os.system('sudo apt-get update')
    os.system('sudo apt-get install libjpeg-dev -y')
    os.system('sudo apt-get install zlib1g-dev -y')
    os.system('sudo apt-get install libfreetype6-dev -y')
    os.system('sudo apt-get install liblcms1-dev -y')
    os.system('sudo apt-get install libopenjp2-7 -y')
    os.system('sudo apt-get install libtiff5 -y')
    os.system('sudo pip3 install pillow')
    os.system('sudo pip3 install pyserial')
    os.system('sudo pip3 install pyautogui')

    print('All done Rebooting in 5 seconds')
    key = input('Press any key to done')
    #if len(key)>0:
    os.system('sudo reboot')
    pass

