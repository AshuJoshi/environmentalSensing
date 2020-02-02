# Environmental Sensing

A project for environmental sensing - various gases, particulate matter, sound and images.

## Part 1: Using RPi Zero W with Sparkfun Qwiic system and sensors - collecting data in AWS Cloud

We start simple - log sensor data to AWS Cloud using a Raspberry Pi Zero W, a Sparkfun Qwiic Hat along with the following sensors:



### IoT Script iot.py

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

## Other Features

- Create and setup a Thing with thing-name
- Delete and clean up a Thing (will NOT work cleanly if the Policy or Thing has versions)
- List Things
- List Certificates
- List Policies


Copy the sampleenv file as .env and provide the specifics - you will need these
