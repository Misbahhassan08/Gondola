from pathlib import Path
import os 
import time 

def install_dep():
    HOME_DIR = Path.home()

    os.system('sudo apt-get update')
    os.system('sudo apt-get install git cmake libpython3-dev python3-numpy python3-pip')
    os.system('sudo pip3 install screeninfo')
    os.system('cd {}'.format(HOME_DIR))
    os.system('git clone --recursive https://github.com/dusty-nv/jetson-inference')
    os.system('cd jetson-inference')
    os.system('mkdir build')
    os.system('cd build')
    os.system('cmake ../')
    os.system('make -j$(nproc)')
    os.system('sudo make install')
    os.system('sudo ldconfig')
    print('All done Rebooting in 5 seconds')
    time.sleep(5)
    os.system('sudo reboot')
    pass

