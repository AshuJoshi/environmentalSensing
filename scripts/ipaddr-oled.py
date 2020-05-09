#!/usr/bin/env python

from __future__ import print_function
import qwiic_micro_oled
import sys
import socket
import time




def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr


if __name__ == '__main__':

    ip = get_ip()
    ipstr = ip.split('.')


    oled = qwiic_micro_oled.QwiicMicroOled()
    oled.begin()

    oled.clear(oled.ALL)
    oled.display()
    time.sleep(1)
    oled.set_font_type(1) 

    oled.clear(oled.PAGE)
        
    oled.set_cursor(0,0)
    oled.print("IP Address:")
    
    oled.set_cursor(0,16)
    oled.print(ipstr[0])
    oled.print(":")
    oled.print(ipstr[1])
    
    oled.set_cursor(0,32)
    oled.print(ipstr[2])
    oled.print(":")
    oled.print(ipstr[3])

    oled.display()