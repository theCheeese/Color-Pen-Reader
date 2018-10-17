import os
import cv2
import numpy as np
from PIL import Image
from glob import glob

def read_img(file):
    img = cv2.imread(file,0)
    img=img.astype(np.float32)
    img-=np.min(img)
    if np.max(img) == 0:
        img+=1
    img/=np.max(img)
    img*=255
    img=img.astype(np.uint8)
    return(img)

def stitch(image1, image2):
    result = np.concatenate((image1, image2), axis=1)
    return result

def mainCombineImages():
    files = os.listdir('/home/pi/Desktop/ColorPenReader/rawImages')
    files = ['/home/pi/Desktop/ColorPenReader/rawImages/' + filename for filename in files]
    files.sort()
    IMG1 = None
    IMG2 = None
   
    #iterate through the files
    for file in files:
        if IMG1 is None:#get first image
            IMG1 = read_img(file)
            IMG3 = IMG1 #save result in case only one exists
            continue
        elif IMG1 is not None and IMG2 is None:
            IMG2 = read_img(file)#get second imagei
            if IMG2 is None:
                continue
            IMG3 = stitch(IMG1,IMG2)#get stitsched output
        elif IMG1 is not None and IMG2 is not None:
            IMG1 = IMG3#consider previous output as first image
            IMG2 = read_img(file)#read next image
            IMG3 = stitch(IMG1,IMG2)#generate stitched output
    Image.fromarray(IMG3).save('/home/pi/Desktop/ColorPenReader/stitched_image.jpg')
