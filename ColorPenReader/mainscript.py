# import stuff
import subprocess
import imagestitch
import Cfilter
import cameracontroller

while True:
    # run camera controller
    cameracontroller.runCamera()
    # run image concatenation
    imagestitch.mainCombineImages()
    # run color filter
    Cfilter.filterColor('/home/pi/Desktop/ColorPenReader/stitched_image.jpg')
    # run OCR and pipe output to TTS
    p2 = subprocess.Popen(["tesseract", "/home/pi/Desktop/ColorPenReader/readyImage.png", "stdout"], stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["festival", "--tts"], stdin=p2.stdout)

