# Environmental Sensing

A project for environmental sensing - various gases, particulate matter, sound and images.

## RPi Zero W, Sparkfun Qwiic Pi Hat & Sensors and AWS Cloud

We start simple - log sensor data to AWS Cloud using a Raspberry Pi Zero W, a Sparkfun Qwiic Hat along with the following sensors:

* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [SparkFun Qwiic Kit for Raspberry Pi](https://www.sparkfun.com/products/15367)
* [Ultrasonic Range Finder - HRXL-MaxSonar-VR](https://www.sparkfun.com/products/11724)

Additionally hooked up a camera with Raspberry Pi to capture images and load them to AWS S3. This is the camera used:
* [Arducam Lens Board SKU B0031](https://www.arducam.com/product/arducam-5mp-m12-picam/)

You could use any other compatible camera as well.

### Setting Up AWS IoT with the script iot.py

A simple script to create Thing, generate a certificate and attach it to the Thing, followed by creating a generic IoT policy, attaching it to the certificate and setting the certificate active. As commands to delete and cleanup things but this version will not handle multiple policy or thing versions.  
The AWS Credentials need to be set in the environment variables. Region has to be specified. 
Run the script from the 05-IoT directory. Keys will be created in the 'keys' subfolder. Download RootCA.pem from the AWS IOT site and copy it in the keys folder. 

```
export AWS_ACCESS_KEY_ID=<your access key id here>
export AWS_SECRET_ACCESS_KEY=<your secrete access key here>
```

The command below will create a Thing called 'wonderbar' - create certiciate attach it, also attach a policy. 
Keys/Pem files are copied in the keys subfolder.

```
python iot.py --region us-east-2 create-and-setup-thing wonderbar

```
The command below reverses the action of creating a thing - deletes everything including the keys in the subfolder.

```
python iot.py --region us-east-2 delete-and-cleanup-thing wonderbar

```

## Other features in the script

- Create and setup a Thing with thing-name
- Delete and clean up a Thing (will NOT work cleanly if the Policy or Thing has versions)
- List Things
- List Certificates
- List Policies

Copy the sampleenv file as .env and provide the specifics - you will need these

### Logging data to AWS

Run the script rpiQwiicAWSIoT.py to read sensor data and log to AWS IoT Core. This script also calls functions in imageCapture.py to take an image and upload it to AWS S3.

```
python3 rpiQwiicAWSIoT.py
```