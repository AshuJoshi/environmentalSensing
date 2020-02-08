from dotenv import load_dotenv
load_dotenv()

from time import sleep
from picamera import PiCamera
import boto3
import os

s3bucket = os.getenv('S3_BUCKET')
camera = PiCamera()

def captureSimpleImageToFile(filenamepath):
    # camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(filenamepath)

def captureResizedImageToFile(filenamepath):
    # camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(filenamepath, resize=(320, 240))

def uploadFileToS3(filename, keyname):
    s3 = boto3.client('s3')
    bucket = s3bucket
    s3.upload_file(filename, bucket, keyname)

if __name__ == '__main__':
    captureSimpleImageToFile('./images/foo.jpg')
    uploadFileToS3('./images/foo.jpg', 'foo.jpg')
