'''

Test module for the Qwiic BME280 and CCS811 (Qwiic Combo without the OLED code, or proximity sensor)

'''

import qwiic

# prox = None
bme = None
ccs = None
# oled = None

def init_qwiic():
    global prox, bme, ccs, oled
    # Qwiic Board define
    # prox = qwiic.QwiicProximity()
    bme = qwiic.QwiicBme280()
    ccs = qwiic.QwiicCcs811()
    # oled = qwiic.QwiicMicroOled()

    # Begin statements 
    # prox.begin()
    bme.begin()
    #ccs.begin()
    # oled.begin()

    # Used for debugging CCS811
    try:
        ccs.begin()    

    except Exception as e:
        print(e)

    # Setup OLED
    # oled.clear(oled.ALL)
    # oled.display()
    # oled.set_font_type(1) 


def read_qwiic(payload):
    global prox, bme, ccs, oled
    #Proximity Sensor variables - these are the available read functions
    #There are additional functions not listed to set thresholds, current, and more
    # proximity = prox.get_proximity()
    # ambient = prox.get_ambient()
    # white = prox.get_white()
    #close = prox.is_close()
    #away = prox.is_away()
    #light = prox.is_light()
    #dark = prox.is_dark()
    #id = prox.get_id()
    
    # BME280 sensor variables
    # reference pressure is available to read or set for altitude calculation
    referencePressure = bme.get_reference_pressure()
    bme.set_reference_pressure(referencePressure)
    pressure = bme.read_pressure()
    # pressure = bme.get_reference_pressure() #in Pa
    altitudem = bme.get_altitude_meters()
    altitudef = bme.get_altitude_feet()
    humidity = bme.read_humidity()
    tempc = bme.get_temperature_celsius()
    tempf = bme.get_temperature_fahrenheit()
    dewc = bme.get_dewpoint_celsius()
    dewf = bme.get_dewpoint_fahrenheit()
    
    #CCS811 sensor variables 
    #ccsbaseline = get_baseline() #used for telling sensor what 'clean' air is
    #set_baseline(ccsbaseline)
    #error = ccs.check_status_error()
    #data = ccs.data_available()
    #app = ccs.app_valid()
    #errorRegister = ccs.get_error_register()
    #ccs.enable_interrupts()
    #ccs.disable_interrupts()
    #ccs.set_drive_mode(mode) #Mode0=Idle, Mode1=read every 1s, Mode2=read every 10s, Mode3=read every 60s, Mode4=RAW mode
    #ccs.set_environmental_data(humidity,temperature)
    
    ccs.read_algorithm_results() #updates the TVOC and CO2 values
    tvoc = ccs.get_tvoc()
    co2 = ccs.get_co2()
    
    #Note:The following values are used when is a NTC thermistor attached to the CCS811 breakout board
    #the environmental combo does not breakout the pins like the breakout board
    #ccs.set_reference_resistance()
    #ccs.read_ntc() #updates temp value
    #ccstemp = ccs.get_temperature() 
    #ccsres = ccs.get_resistance()

    # print ("BME Temperature %.1f F" %tempf)
    # print ("Humidity %.1f" %humidity)
    # print ("Pressure %.2f Pa" %pressure)
    # print ("Altitude %.2f ft" %altitudef)
    # print ("CCS Temperature %.1f F" %ccstemp)
    # print ("Distance %.2f " %proximity)
    # print ("Ambient Light %.2f" %ambient)
    # print ("TVOC %.2f" %tvoc)
    # print ("CO2 %.2f" %co2)
    # print (" ") #blank line for easier readability
    
    payload['tempc'] = round(tempc, 3)
    payload['tempf'] = round(tempf, 3)
    payload['humidity'] = round(humidity, 3)
    payload['pressure'] = round(pressure/1000, 3)

    payload['tvoc'] = tvoc
    payload['co2'] = co2
    # payload['proximity'] = proximity
    # payload['ambient'] = ambient

    # oled.clear(oled.PAGE)
    
    # oled.set_cursor(0,0)
    # oled.print("Tmp:")
    # oled.print(int(tempf))
    # oled.print("F")
    #oled.print(int(temc))
    #oled.print("C")
    
    # oled.set_cursor(0,16)
    # oled.print("RH%:") #Relative Humidity
    # oled.print(int(humidity))
    
    # oled.set_cursor(0,32)
    # oled.print("hPa:") #hPa is a more typical output and helps with spacing
    # oled.print(int(pressure/100))
    # oled.display()

    return(payload)