import picamera
import RPi.GPIO as GPIO
import shutil
import os
import time

photo_num = 0

def runCamera():
    #set up camera
    camera = picamera.PiCamera(framerate=90, sensor_mode=7)
    camera.resolution = (640, 480)
    camera.start_preview()

    #set up callback method
    def captureImage(channel):
        global photo_num
        camera.capture('rawImages/' + str(photo_num) + '.jpg')
        photo_num += 1

    #Pin numbering
    IS_SCANNING = 3
    CAPTURE_INTERRUPT = 5
    RPI_READY = 7

    #IO setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IS_SCANNING, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CAPTURE_INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RPI_READY, GPIO.OUT)

    #delete the rawImages folder and recreate it
    shutil.rmtree('/home/pi/Desktop/ColorPenReader/rawImages')
    os.mkdir('rawImages')

    #get ready for scanning
    GPIO.output(RPI_READY, True)

    #when isScanning is low, waiting for isScanning goes to high
    while GPIO.input(IS_SCANNING) == True:
        pass

    #when isScanning is high, call captureImage() whenever CaptureInterrupt rising edge is detected
    if GPIO.input(IS_SCANNING) == False:    
        GPIO.add_event_detect(CAPTURE_INTERRUPT, GPIO.RISING, callback=captureImage, bouncetime=100)
        time.sleep(0.01)
        while GPIO.input(IS_SCANNING) == False:
            pass    

    camera.stop_preview()
    time.sleep(1)
    camera.close()
    GPIO.cleanup()
