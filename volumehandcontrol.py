import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import math
import osascript


################
wcam ,hcam =640,480
####################

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4,hcam)
pTime =0
cTime =0

detector = htm.handDetector(detectionCon=0.7)
minvol = 50
maxvol = 240



while True:
    succes,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    outputVol = 0



    if len(lmList) !=0:
        # print(lmList[4],lmList[8])
        outvol = 0 
        x1, y1 =lmList[4][1],lmList[4][2]
        x2, y2 =lmList[8][1],lmList[8][2]
       
        cx,cy = (x1+x2)//2 , (y1+y2) //2


        cv2.circle(
            img,(x1,y1),15,(255,0,255),cv2.FILLED
        )
        cv2.circle(
            img,(x2,y2),15,(255,0,255),cv2.FILLED
        )

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        cv2.circle(
            img,(cx,cy),15,(255,0,255),cv2.FILLED
        )

        length = math.hypot(
            x2 - x1 ,y2 - y1
        )
        # print(length)
        # target_volume = (length - minvol)*100/(maxvol-minvol)

        target_volume = np.interp(length,[50,240],[0,100])
        vol = "set volume output volume " + str(target_volume)
        osascript.osascript(vol)

        result = osascript.osascript('get volume settings')
        volInfo = result[1].split(',')
        outputVol = volInfo[0].replace('output volume:', '')
        print(int(length),outputVol)
        

        if length < 50:
             cv2.circle(
            img,(cx,cy),15,(0,255,0),cv2.FILLED
        )
    cv2.putText(img,f'{outputVol}%',(50,400),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

       
   
    cTime =time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)

    cv2.imshow("img",img)
    if cv2.waitKey(1) == ord('q'):
        break