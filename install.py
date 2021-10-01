from pathlib import Path
import os 
import time 

def install_dep():
    HOME_DIR = Path.home()



    os.system('sudo apt-get update')
    os.system('sudo apt-get install git cmake libpython3-dev python3-numpy python3-pip nano python3-scipy python3-h5py python3-pil curl update upgrade  -y')
    os.system('sudo pip3 install screeninfo')

    # ----------------- auto start script -----------------------------------------------------------------
    try:
        script_file = '{}/startscript.sh'.format(HOME_DIR)
        if (Path.exists(script_file) == False):
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
        if (Path.exists(outFileName) == False):
            outFileName = '{}/.config/autostart/pythonscript.desktop'.format(HOME_DIR)
            outFile=open(outFileName, "w")
            outFile.write("""
            Desktop Entry]
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
        
    except  Exception as error:
        print(error)
        v = str(input('press a to restart b to continue'))
        if v == "a" or v == "A":
            os.system('sudo reboot')
        else:
            pass


    os.system('cd {} && git clone --recursive https://github.com/dusty-nv/jetson-inference'.format(HOME_DIR))
    os.system('mkdir {}/jetson-inference/build'.format(HOME_DIR))

    os.system('cd {}/jetson-inference/build && sudo cmake ../'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo make -j$(nproc)'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo make install'.format(HOME_DIR))
    os.system('cd {}/jetson-inference/build && sudo ldconfig'.format(HOME_DIR))

    print('All done Rebooting in 5 seconds')
    key = input('Press any key to done')
    #if len(key)>0:
    os.system('sudo reboot')
    pass

