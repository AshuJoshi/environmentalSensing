#!/usr/bin/python3
import time

from atlasph.AtlasI2C import (
	 AtlasI2C
)

device = AtlasI2C(address = 99, moduletype = 'pH', name = 'STPH')

def get_ezo_ph():
    
    # device_list = get_devices()
    # device = device_list[0]
    # First device in array is Atlas Scientific 
    device.write("R")
    time.sleep(2)
    return device.read()
                    
# if __name__ == '__main__':
#     get_ezo_ph()