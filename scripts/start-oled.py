#!/usr/bin/env python

from __future__ import print_function
import qwiic_micro_oled
import sys
import socket
import time


if __name__ == '__main__':

    oled = qwiic_micro_oled.QwiicMicroOled()
    oled.begin()

    oled.clear(oled.ALL)
    oled.display()
    time.sleep(1)

    oled.set_font_type(1) 
    oled.clear(oled.PAGE)
        
    oled.set_cursor(0,0)
    oled.print("Init Script")
    
    oled.set_cursor(0,16)
    oled.print("Boot Done")
    

    oled.display()