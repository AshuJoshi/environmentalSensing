# created by Noah Coad on 2020-02-07 for AWS PepsiCo LATAM project
# see also ~/code/py/learn/learn_pyserial_rs232.py
# 
# prereqs
# pip3 install --user pyserial
 
# library imports
import serial, time, sys
 
# port definitions on RPi vs mac
port = {'linux': '/dev/serial0', 'darwin': '/dev/cu.usbserial'}[sys.platform]
# create a serial port connection
s = serial.Serial(port, 9600)
print(f"Using port: {port}")

# get a current reading
def read_ultrasonic():
    # read the latest distance in the serial buffer
    while (s.in_waiting): data = s.read_until(b'\r')

    # decode the distance reading
    dist = int(data.decode("utf-8")[1:])

    # show user
    # print(f"distance: {dist}mm, raw: {data}");
    return dist

if __name__ == '__main__':
    # application run loop
    print("running, press ctrl+c to quit")
    while (True):
        # if there is data waiting in the buffer, read i
        if (s.in_waiting > 0): read_ultrasonic()
        # pause
        time.sleep(1)
