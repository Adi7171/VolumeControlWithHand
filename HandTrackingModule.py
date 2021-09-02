import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode =False,maxhands = 2 , detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxhands=maxhands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands= mp.solutions.hands
        self.hands = self.mpHands.Hands( self.mode,self.maxhands,self.detectionCon,self.trackCon) #uses only RGB
        self.mpDraw = mp.solutions.drawing_utils # to get lines between the points in a hand

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # process frame and give us result 
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:# handlms is for one hand result
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)#when you add HANDCONNECTIONS then it darws the line betweeen the pointsß
        return img


                # for handLms in results.multi_hand_landmarks:
                # for id,lm in enumerate(handLms.landmark):
                #     # print(id,lm)
                #     h,w,c = img.shape
                #     cx,cy = int(lm.x*w),int(lm.y*h)
                #     print(id,cx,cy)
                #     if id ==0 & id == 5 & id== 6 & id ==7 & id==8:
                #         cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)

    def findPosition(self,img,handNo=0,draw =True):
            lmList =[]
            if self.results.multi_hand_landmarks:
                myHand =self.results.multi_hand_landmarks[handNo]

                for id,lm in enumerate(myHand.landmark):
                        # print(id,lm)
                        h,w,c = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        # print(id,cx,cy)
                        lmList.append([id,cx,cy])
                        if draw:
                            cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
            return lmList


  
   

def main():
    vid =cv2.VideoCapture(0)

    pTime=0
    cTime=0
    detector = handDetector()
    while True:
        success,img = vid.read()
        img = detector.findHands(img)
        
        lmList=detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])

        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_TRIPLEX,3,(255,0,255),3)

        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

  

if __name__ == '__main__':
    main()