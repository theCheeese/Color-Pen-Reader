import cv2
import numpy as np 
import os
#detection

def filterColorManyFiles(filepath):
    files = os.listdir(filepath)
    for filename in files:
        filterColor(filename)

def filterColor(filename):
    def Odetection(Om,On,Os,Os1):
        
        if hierarchy is None or contours is None:
            return
        
        for k in hierarchy[0,0:X-3,2]:
            Olst2.append(k)
        ##print(Olst2)

        while (Om<X-4 and On<X):
            Om +=1
            On +=1
            for i in hierarchy[0,Om:On,2]:
                Os += i    
            Olst.append(Os)
            Os = 0
    
            for i1 in hierarchy[0,Om:On,3]:
                Os1 += i1    
            Olst1.append(Os1)
            Os1 = 0
        ##print(Olst1)

        for l in range(0,len(Olst)):
            if (Olst[l] == 3*Olst2[l]+2 and Olst1[l] == 3*Olst2[l]-1):
                cv2.drawContours(img,contours,Olst2[l]-1,(255,255,255),-1)
                cv2.drawContours(img,contours,Olst2[l]+1,(0,0,0),-1) 

    def Ldetection(Lm,Ln,Ls,Ls1):

        if hierarchy is None or contours is None:
            return

        for k in hierarchy[0,0:X-1,2]:
            Llst2.append(k)
        ##print(Llst2)

        while  (Lm<X-2 and Ln<X):
            Lm +=1
            Ln +=1
            for i in hierarchy[0,Lm:Ln,2]:
                Ls += i    
            Llst.append(Ls)
            Ls = 0
    
            for i1 in hierarchy[0,Lm:Ln,3]:
                Ls1 += i1    
            Llst1.append(Ls1)
            Ls1 = 0
        ##print(Llst)
        if contours is None:
            return

        for l in range(0,len(Llst2)):
            if (Llst[l] == Llst2[l]-1 and Llst1[l] == Llst2[l]-2):
                cv2.drawContours(img,contours,Llst2[l]-1,(255,255,255),-1)

    def Bdetection(m,n,s,s1):

        if hierarchy is None or contours is None:
            return

        for k in hierarchy[0,0:X-5,2]:
            lst2.append(k)

        while  (m<X-6 and n<X):
            m +=1
            n +=1
            for i in hierarchy[0,m:n,2]:
                s += i    
        #print(s)
            lst.append(s)
            s = 0
    
            for i1 in hierarchy[0,m:n,3]:
                s1 += i1    
        #print(s1)
            lst1.append(s1)
            s1 = 0

        if contours is None:
            return

        for l in range(0,len(lst)):
            if (lst[l] == 4*lst2[l]+5 and lst1[l] == 5*lst2[l]+2):
                cv2.drawContours(img,contours,lst2[l]-1,(255,255,255),-1)
                cv2.drawContours(img,contours,lst2[l]+1,(0,0,0),-1) 
                cv2.drawContours(img,contours,lst2[l]+3,(0,0,0),-1) 
    #main code

    img = cv2.imread(filename)
    img = cv2.bilateralFilter(img,50,120,120) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(img, 66, 198)  

    ret, binary = cv2.threshold(canny,127,255,cv2.THRESH_BINARY)  
   
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)[-2:]  
    if contours is not None:
        cv2.drawContours(binary,contours,-1,(255,255,255),2)

    #cv2.imshow("img", binary)
    #k = cv2.waitKey(0)
    #if k == 27:                 # wait for ESC key to exit
    #    cv2.destroyAllWindows()
    #elif k == ord('s'):        # wait for 's' key to save and exit
    cv2.imwrite(filename, binary)
    #    cv2.destroyAllWindows()

##define parameter
    m = -1
    n = 5
    s = 0
    s1 = 0
    lst = []
    lst1 = []
    lst2 = []

    Om = -1
    On = 3
    Os = 0
    Os1 = 0
    Olst = []
    Olst1 = []
    Olst2 = []

    Lm = -1
    Ln = 1
    Ls = 0
    Ls1 = 0
    Llst = []
    Llst1 = []
    Llst2 = []

#read pic
    img = cv2.imread(filename)  
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
    ret, binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)  
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    if hierarchy is not None:
        X = hierarchy.shape[1]
    else:
        X = 0

    if X>=6:
        Ldetection(Lm,Ln,Ls,Ls1)
        Odetection(Om,On,Os,Os1)
        Bdetection(m,n,s,s1)
    elif X>=4:
        Ldetection(Lm,Ln,Ls,Ls1)
        Odetection(Om,On,Os,Os1)
    elif X>=2:
        Ldetection(Lm,Ln,Ls,Ls1)
    else:
        pass

##inverse pic and display
    image2 = img.copy()    
    for i in range(0,img.shape[0]):  
        for j in range(0,img.shape[1]):  
            image2[i,j]= 255 - img[i,j]  

    #cv2.imshow('image2',image2)
    cv2.imwrite('/home/pi/Desktop/ColorPenReader/readyImage.png', image2)  
    #cv2.waitKey(0) 
