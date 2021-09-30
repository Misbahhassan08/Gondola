from pathlib import Path
import os 
import time 

def install_dep():
    HOME_DIR = Path.home()

    os.system('sudo apt-get update')
    os.system('sudo apt-get install git cmake libpython3-dev python3-numpy python3-pip')
    os.system('sudo pip3 install screeninfo')
    os.system('git clone --recursive https://github.com/dusty-nv/jetson-inference')
    os.system('mkdir {}/jetson-inference/build'.format(HOME_DIR))
    os.system('{}/jetson-inference/build/cmake ../'.format(HOME_DIR))
    os.system('{}/jetson-inference/build/make -j$(nproc)'.format(HOME_DIR))
    os.system('sudo {}/jetson-inference/build/make install'.format(HOME_DIR))
    os.system('sudo {}/jetson-inference/build/ldconfig'.format(HOME_DIR))
    print('All done Rebooting in 5 seconds')
    time.sleep(5)
    os.system('sudo reboot')
    pass

