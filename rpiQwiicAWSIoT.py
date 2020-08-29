#!/usr/bin/env python3
'''

A Python script for Pi Zero with a Sparkfun Qwiic Hat, reading the combo
sensor - BME280 and CCS811 and logging data to the AWS IoT Core

'''
from __future__ import print_function, division
from dotenv import load_dotenv
load_dotenv()

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import datetime
import json
import os
import sys


host = os.getenv('AWS_IOT_HOST')
clientId = os.getenv('THING_NAME')
port = 8883
rootCAPath = os.getenv('ROOT_CA_PATH')
certificatePath = os.getenv('CERT_PATH')
privateKeyPath = os.getenv('PRV_KEY_PATH')
topic = os.getenv('TOPIC')
loopDelay = os.getenv('LOOP_DELAY')
ULTRA_ENABLE = bool(os.getenv('ULTRA_ENABLE'))
S3_ENABLE = bool(os.getenv('S3_ENABLE'))
RESIZED_IMAGE = bool(os.getenv('RESIZED_IMAGE'))
ATLASPH_ENABLE = bool(os.getenv('ATLASPH_ENABLE'))
ADIMW_ENABLE = bool(os.getenv('ADIMW_ENABLE'))
QWIIC_ENABLE = bool(os.getenv('QWIIC_ENABLE'))

if ATLASPH_ENABLE:
    sys.path.append('./atlasph')
    import atlasph.ezophi2c as ezophi2c
if ULTRA_ENABLE:
    from helperlib.ultrasonic import read_ultrasonic
if QWIIC_ENABLE:
    # import helperlib.qwiicsensor as q
    import helperlib.qwiic811280 as q
if S3_ENABLE:
    import imageCapture as img

# These values are used to give BME280 and CCS811 some time to take samples
if QWIIC_ENABLE:
    initialize=True
    n=2
    q.init_qwiic()

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    try:
        payload = {}
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
        payload['timestamp'] = round(ts)
        payload['time'] = st
        # print (time.strftime("%a %b %d %Y %I:%M:%S%p", time.localtime())) #12-hour time
        if QWIIC_ENABLE:
            if initialize==True:
                print ("Initializing: BME280 and CCS811 are taking samples before printing and publishing data!")
                print (" ")
            else:
                #print ("Finished initializing")
                n=1 #set n back to 1 to read sensor data once in loop
            for n in range (0,n):
                #print ("n = ", n) #used for debugging for loop
                q.read_qwiic(payload)
                #Give some time for the BME280 and CCS811 to initialize when starting up
                if initialize==True:
                    time.sleep(10)
                    initialize=False
        
        if ULTRA_ENABLE:
            payload['ultrasonic'] = read_ultrasonic()

        if S3_ENABLE:
            keyname = clientId + '-' + str(payload['timestamp']) 
            filename = './images/' + keyname + '.jpeg'
            if RESIZED_IMAGE:
                img.captureResizedImageToFile(filename)
            else:
                img.captureSimpleImageToFile(filename)

            img.uploadFileToS3(filename, (keyname + '.jpeg'))

            if os.path.exists(filename):
                os.remove(filename)
            else:
                print('File does not exist: ', filename)

            payload['image'] = keyname

        if ATLASPH_ENABLE:
            atlasph = ezophi2c.get_ezo_ph()
            atlasph = float(atlasph.rstrip('\x00'))
            payload['as_ph_value'] = atlasph

        messageJson = json.dumps(payload)
        # use clientId / ThingName as the topic for publishing the payload
        pubTopic = topic + '/' + clientId
        myAWSIoTMQTTClient.publish(pubTopic, messageJson, 1)
        
        print(payload)
        print (" ") #blank line for easier readability

        #delay (number of seconds) so we are not constantly displaying data and overwhelming devices
        time.sleep(int(loopDelay))
            
    #if we break things or exit then exit cleanly
    except (EOFError, SystemExit, KeyboardInterrupt):
        # mqttc.disconnect()
        sys.exit()